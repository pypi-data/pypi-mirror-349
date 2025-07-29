"""
Intervals.icu MCP Server

This module implements a Model Context Protocol (MCP) server for connecting
Claude with the Intervals.icu API. It provides tools for retrieving and managing
athlete data, including activities, events, workouts, and wellness metrics.

Key features:
- Activity retrieval and detailed analysis
- Event management (races, workouts, calendar items)
- Wellness data tracking and visualization
- Error handling with user-friendly messages
- Configurable parameters with environment variable support

The server follows MCP specifications and uses the Python MCP SDK.

The server is designed to be run as a standalone script.
"""

from json import JSONDecodeError
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# Import formatting utilities
from intervals_mcp_server.utils.formatting import (
    format_activity_summary,
    format_event_details,
    format_event_summary,
    format_intervals,
    format_wellness_entry,
)

# Try to load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv

    _ = load_dotenv()
except ImportError:
    # python-dotenv not installed, proceed without it
    pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("intervals_icu_mcp_server")

# Create a single AsyncClient instance for all requests
httpx_client = httpx.AsyncClient()


@asynccontextmanager
async def lifespan(app: FastMCP):
    """Ensure the shared httpx client is closed when the server stops."""
    try:
        yield
    finally:
        await httpx_client.aclose()


# Initialize FastMCP server with custom lifespan
mcp = FastMCP("intervals-icu", lifespan=lifespan)

# Constants
INTERVALS_API_BASE_URL = os.getenv(
    "INTERVALS_API_BASE_URL", "https://intervals.icu/api/v1"
)
API_KEY = os.getenv("API_KEY", "")  # Provide default empty string
ATHLETE_ID = os.getenv("ATHLETE_ID", "")  # Default athlete ID from .env
USER_AGENT = "intervalsicu-mcp-server/1.0"


async def make_intervals_request(
    url: str, api_key: str | None = None, params: dict[str, Any] | None = None
) -> dict[str, Any] | list[dict[str, Any]]:
    """Make a GET request to the Intervals.icu API with proper error handling."""

    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}

    # Use provided api_key or fall back to global API_KEY
    key_to_use = api_key if api_key is not None else API_KEY
    auth = httpx.BasicAuth("API_KEY", key_to_use)
    full_url = f"{INTERVALS_API_BASE_URL}{url}"

    try:
        response = await httpx_client.get(
            full_url, headers=headers, params=params, auth=auth, timeout=30.0
        )
        try:
            data = response.json() if response.content else {}
        except JSONDecodeError:
            logger.error("Invalid JSON in response from: %s", full_url)
            return {"error": True, "message": "Invalid JSON in response"}
        _ = response.raise_for_status()
        return data
    except httpx.HTTPStatusError as e:
        error_code = e.response.status_code
        error_text = e.response.text

        logger.error("HTTP error: %s - %s", error_code, error_text)

        # Provide specific messages for common error codes
        error_messages = {
            HTTPStatus.UNAUTHORIZED: f"{HTTPStatus.UNAUTHORIZED.value} {HTTPStatus.UNAUTHORIZED.phrase}: Please check your API key.",
            HTTPStatus.FORBIDDEN: f"{HTTPStatus.FORBIDDEN.value} {HTTPStatus.FORBIDDEN.phrase}: You may not have permission to access this resource.",
            HTTPStatus.NOT_FOUND: f"{HTTPStatus.NOT_FOUND.value} {HTTPStatus.NOT_FOUND.phrase}: The requested endpoint or ID doesn't exist.",
            HTTPStatus.UNPROCESSABLE_ENTITY: f"{HTTPStatus.UNPROCESSABLE_ENTITY.value} {HTTPStatus.UNPROCESSABLE_ENTITY.phrase}: The server couldn't process the request (invalid parameters or unsupported operation).",
            HTTPStatus.TOO_MANY_REQUESTS: f"{HTTPStatus.TOO_MANY_REQUESTS.value} {HTTPStatus.TOO_MANY_REQUESTS.phrase}: Too many requests in a short time period.",
            HTTPStatus.INTERNAL_SERVER_ERROR: f"{HTTPStatus.INTERNAL_SERVER_ERROR.value} {HTTPStatus.INTERNAL_SERVER_ERROR.phrase}: The Intervals.icu server encountered an internal error.",
            HTTPStatus.SERVICE_UNAVAILABLE: f"{HTTPStatus.SERVICE_UNAVAILABLE.value} {HTTPStatus.SERVICE_UNAVAILABLE.phrase}: The Intervals.icu server might be down or undergoing maintenance.",
        }

        # Get a specific message or default to the server's response
        try:
            status = HTTPStatus(error_code)
            custom_message = error_messages.get(status, error_text)
        except ValueError:
            # If the status code doesn't map to HTTPStatus, use the error_text
            custom_message = error_text

        return {"error": True, "status_code": error_code, "message": custom_message}
    except httpx.RequestError as e:
        logger.error("Request error: %s", str(e))
        return {"error": True, "message": f"Request error: {str(e)}"}
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        return {"error": True, "message": f"Unexpected error: {str(e)}"}


# ----- MCP Tool Implementations ----- #


@mcp.tool()
async def get_activities(
    athlete_id: str | None = None,
    api_key: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    limit: int = 10,
    include_unnamed: bool = False,
) -> str:
    """Get a list of activities for an athlete from Intervals.icu

    Args:
        athlete_id: The Intervals.icu athlete ID (optional, will use ATHLETE_ID from .env if not provided)
        api_key: The Intervals.icu API key (optional, will use API_KEY from .env if not provided)
        start_date: Start date in YYYY-MM-DD format (optional, defaults to 30 days ago)
        end_date: End date in YYYY-MM-DD format (optional, defaults to today)
        limit: Maximum number of activities to return (optional, defaults to 10)
        include_unnamed: Whether to include unnamed activities (optional, defaults to False)
    """
    # Use provided athlete_id or fall back to global ATHLETE_ID
    athlete_id_to_use = athlete_id if athlete_id is not None else ATHLETE_ID
    if not athlete_id_to_use:
        return "Error: No athlete ID provided and no default ATHLETE_ID found in environment variables."

    # Parse date parameters
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    # Fetch more activities if we need to filter out unnamed ones
    api_limit = limit * 3 if not include_unnamed else limit

    # Call the Intervals.icu API
    params = {"oldest": start_date, "newest": end_date, "limit": api_limit}

    result = await make_intervals_request(
        url=f"/athlete/{athlete_id_to_use}/activities", api_key=api_key, params=params
    )

    # Check for error differently based on result type
    if isinstance(result, dict) and "error" in result:
        error_message = result.get("message", "Unknown error")
        return f"Error fetching activities: {error_message}"

    # Format the response
    if not result:
        return f"No activities found for athlete {athlete_id_to_use} in the specified date range."

    # Ensure result is a list of activity dictionaries
    activities: list[dict[str, Any]] = []

    if isinstance(result, list):
        # Result is already a list
        activities = [item for item in result if isinstance(item, dict)]
    elif isinstance(result, dict):
        # Result is a single activity or a container
        for key, value in result.items():
            if isinstance(value, list):
                # Found a list inside the dictionary
                activities = [item for item in value if isinstance(item, dict)]
                break
        # If no list was found but the dict has typical activity fields, treat it as a single activity
        if not activities and any(
            key in result for key in ["name", "startTime", "distance"]
        ):
            activities = [result]

    if not activities:
        return f"No valid activities found for athlete {athlete_id_to_use} in the specified date range."

    # Filter out unnamed activities if needed and limit to requested count
    if not include_unnamed:
        activities = [
            activity
            for activity in activities
            if activity.get("name") and activity.get("name") != "Unnamed"
        ]

        # If we don't have enough named activities, try to fetch more
        if len(activities) < limit:
            # Calculate how far back we need to go to get more activities
            oldest_date = datetime.fromisoformat(start_date)
            older_start_date = (oldest_date - timedelta(days=60)).strftime("%Y-%m-%d")
            older_end_date = (oldest_date - timedelta(days=1)).strftime("%Y-%m-%d")

            # Additional fetch if needed
            if older_start_date < older_end_date:
                more_params = {
                    "oldest": older_start_date,
                    "newest": older_end_date,
                    "limit": api_limit,
                }
                more_result = await make_intervals_request(
                    url=f"/athlete/{athlete_id_to_use}/activities",
                    api_key=api_key,
                    params=more_params,
                )

                if isinstance(more_result, list):
                    more_activities = [
                        activity
                        for activity in more_result
                        if isinstance(activity, dict)
                        and activity.get("name")
                        and activity.get("name") != "Unnamed"
                    ]
                    activities.extend(more_activities)

    # Limit to requested count
    activities = activities[:limit]

    if not activities:
        if include_unnamed:
            return f"No valid activities found for athlete {athlete_id_to_use} in the specified date range."
        else:
            return f"No named activities found for athlete {athlete_id_to_use} in the specified date range. Try with include_unnamed=True to see all activities."

    activities_summary = "Activities:\n\n"
    for activity in activities:
        if isinstance(activity, dict):
            activities_summary += format_activity_summary(activity) + "\n"
        else:
            activities_summary += f"Invalid activity format: {activity}\n\n"

    return activities_summary


@mcp.tool()
async def get_activity_details(activity_id: str, api_key: str | None = None) -> str:
    """Get detailed information for a specific activity from Intervals.icu

    Args:
        activity_id: The Intervals.icu activity ID
        api_key: The Intervals.icu API key (optional, will use API_KEY from .env if not provided)
    """
    # Call the Intervals.icu API
    result = await make_intervals_request(
        url=f"/activity/{activity_id}", api_key=api_key
    )

    if isinstance(result, dict) and "error" in result:
        error_message = result.get("message", "Unknown error")
        return f"Error fetching activity details: {error_message}"

    # Format the response
    if not result:
        return f"No details found for activity {activity_id}."

    # If result is a list, use the first item if available
    activity_data = result[0] if isinstance(result, list) and result else result
    if not isinstance(activity_data, dict):
        return f"Invalid activity format for activity {activity_id}."

    # Return a more detailed view of the activity
    detailed_view = format_activity_summary(activity_data)

    # Add additional details if available
    if "zones" in activity_data:
        zones = activity_data["zones"]
        detailed_view += "\nPower Zones:\n"
        for zone in zones.get("power", []):
            detailed_view += (
                f"Zone {zone.get('number')}: {zone.get('secondsInZone')} seconds\n"
            )

        detailed_view += "\nHeart Rate Zones:\n"
        for zone in zones.get("hr", []):
            detailed_view += (
                f"Zone {zone.get('number')}: {zone.get('secondsInZone')} seconds\n"
            )

    return detailed_view


@mcp.tool()
async def get_events(
    athlete_id: str | None = None,
    api_key: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> str:
    """Get events for an athlete from Intervals.icu

    Args:
        athlete_id: The Intervals.icu athlete ID (optional, will use ATHLETE_ID from .env if not provided)
        api_key: The Intervals.icu API key (optional, will use API_KEY from .env if not provided)
        start_date: Start date in YYYY-MM-DD format (optional, defaults to today)
        end_date: End date in YYYY-MM-DD format (optional, defaults to 30 days from today)
    """
    # Use provided athlete_id or fall back to global ATHLETE_ID
    athlete_id_to_use = athlete_id if athlete_id is not None else ATHLETE_ID
    if not athlete_id_to_use:
        return "Error: No athlete ID provided and no default ATHLETE_ID found in environment variables."

    # Parse date parameters
    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")
    if not end_date:
        end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    # Call the Intervals.icu API
    params = {"oldest": start_date, "newest": end_date}

    result = await make_intervals_request(
        url=f"/athlete/{athlete_id_to_use}/events", api_key=api_key, params=params
    )

    if isinstance(result, dict) and "error" in result:
        error_message = result.get("message", "Unknown error")
        return f"Error fetching events: {error_message}"

    # Format the response
    if not result:
        return f"No events found for athlete {athlete_id_to_use} in the specified date range."

    # Ensure result is a list
    events = result if isinstance(result, list) else []

    if not events:
        return f"No events found for athlete {athlete_id_to_use} in the specified date range."

    events_summary = "Events:\n\n"
    for event in events:
        if not isinstance(event, dict):
            continue

        events_summary += format_event_summary(event) + "\n\n"

    return events_summary


@mcp.tool()
async def get_event_by_id(
    event_id: str,
    athlete_id: str | None = None,
    api_key: str | None = None,
) -> str:
    """Get detailed information for a specific event from Intervals.icu

    Args:
        event_id: The Intervals.icu event ID
        athlete_id: The Intervals.icu athlete ID (optional, will use ATHLETE_ID from .env if not provided)
        api_key: The Intervals.icu API key (optional, will use API_KEY from .env if not provided)
    """
    # Use provided athlete_id or fall back to global ATHLETE_ID
    athlete_id_to_use = athlete_id if athlete_id is not None else ATHLETE_ID
    if not athlete_id_to_use:
        return "Error: No athlete ID provided and no default ATHLETE_ID found in environment variables."

    # Call the Intervals.icu API
    result = await make_intervals_request(
        url=f"/athlete/{athlete_id_to_use}/event/{event_id}", api_key=api_key
    )

    if isinstance(result, dict) and "error" in result:
        error_message = result.get("message", "Unknown error")
        return f"Error fetching event details: {error_message}"

    # Format the response
    if not result:
        return f"No details found for event {event_id}."

    if not isinstance(result, dict):
        return f"Invalid event format for event {event_id}."

    return format_event_details(result)


@mcp.tool()
async def get_wellness_data(
    athlete_id: str | None = None,
    api_key: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> str:
    """Get wellness data for an athlete from Intervals.icu

    Args:
        athlete_id: The Intervals.icu athlete ID (optional, will use ATHLETE_ID from .env if not provided)
        api_key: The Intervals.icu API key (optional, will use API_KEY from .env if not provided)
        start_date: Start date in YYYY-MM-DD format (optional, defaults to 30 days ago)
        end_date: End date in YYYY-MM-DD format (optional, defaults to today)
    """
    # Use provided athlete_id or fall back to global ATHLETE_ID
    athlete_id_to_use = athlete_id if athlete_id is not None else ATHLETE_ID
    if not athlete_id_to_use:
        return "Error: No athlete ID provided and no default ATHLETE_ID found in environment variables."

    # Parse date parameters
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    # Call the Intervals.icu API
    params = {"oldest": start_date, "newest": end_date}

    result = await make_intervals_request(
        url=f"/athlete/{athlete_id_to_use}/wellness", api_key=api_key, params=params
    )

    if isinstance(result, dict) and "error" in result:
        return f"Error fetching wellness data: {result.get('message')}"

    # Format the response
    if not result:
        return f"No wellness data found for athlete {athlete_id_to_use} in the specified date range."

    wellness_summary = "Wellness Data:\n\n"

    # Handle both list and dictionary responses
    if isinstance(result, dict):
        for date_str, data in result.items():
            # Add the date to the data dictionary if it's not already presen
            if isinstance(data, dict) and "date" not in data:
                data["date"] = date_str
            wellness_summary += format_wellness_entry(data) + "\n\n"
    elif isinstance(result, list):
        for entry in result:
            if isinstance(entry, dict):
                wellness_summary += format_wellness_entry(entry) + "\n\n"

    return wellness_summary


@mcp.tool()
async def get_activity_intervals(activity_id: str, api_key: str | None = None) -> str:
    """Get interval data for a specific activity from Intervals.icu

    This endpoint returns detailed metrics for each interval in an activity, including power, heart rate,
    cadence, speed, and environmental data. It also includes grouped intervals if applicable.

    Args:
        activity_id: The Intervals.icu activity ID
        api_key: The Intervals.icu API key (optional, will use API_KEY from .env if not provided)
    """
    # Call the Intervals.icu API
    result = await make_intervals_request(
        url=f"/activity/{activity_id}/intervals", api_key=api_key
    )

    if isinstance(result, dict) and "error" in result:
        error_message = result.get("message", "Unknown error")
        return f"Error fetching intervals: {error_message}"

    # Format the response
    if not result:
        return f"No interval data found for activity {activity_id}."

    # If the result is empty or doesn't contain expected fields
    if not isinstance(result, dict) or not any(
        key in result for key in ["icu_intervals", "icu_groups"]
    ):
        return f"No interval data or unrecognized format for activity {activity_id}."

    # Format the intervals data
    return format_intervals(result)


# Run the server
if __name__ == "__main__":
    mcp.run()
