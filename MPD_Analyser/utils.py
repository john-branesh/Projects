# utils.py
import re
from datetime import timedelta

# Parses ISO 8601 duration strings (e.g., "PT1H30M", "PT45S") into timedelta objects
# Format: PT[hours]H[minutes]M[seconds]S (all components optional)
def parse_iso_duration(duration):
    # Return None if no duration string provided
    if not duration:
        return None

    # Match ISO 8601 duration pattern: PT followed by optional hours, minutes, seconds
    # Example matches: "PT1H30M45S", "PT30M", "PT45S"
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if not match:
        return None  # Invalid format

    # Extract hours, minutes, seconds (default to "0" if not present)
    h, m, s = match.groups(default="0")
    
    # Convert to timedelta object
    return timedelta(hours=int(h), minutes=int(m), seconds=int(s))


# Formats a timedelta object into a human-readable string
# Examples: "1h 30m 45s" or "30m 45s" (hours omitted if zero)
def format_timedelta(td):
    # Return "Not specified" for None or empty timedelta
    if not td:
        return "Not specified"

    # Convert timedelta to total seconds
    total = int(td.total_seconds())
    
    # Calculate hours, minutes, and seconds
    h, rem = divmod(total, 3600)  # 3600 seconds = 1 hour
    m, s = divmod(rem, 60)         # 60 seconds = 1 minute

    # Format with hours if present, otherwise just minutes and seconds
    if h:
        return f"{h}h {m:02d}m {s:02d}s"
    return f"{m}m {s:02d}s"
