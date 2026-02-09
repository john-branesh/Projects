# extract_periods.py
from datetime import timedelta
from utils import parse_iso_duration, format_timedelta

# Extracts and constructs a timeline of all periods in an MPD document
# Calculates start, duration, and end times for each period, handling both explicit and derived values
def extract_period_timeline(root, ns):
    # Find all Period elements in the MPD
    periods = root.findall("dash:Period", ns)
    timeline = []  # List to store period information
    current_start = timedelta()  # Track the running start time for periods without explicit start

    # Process each period sequentially
    for idx, p in enumerate(periods):
        # Check if period has an explicit start time attribute
        start_attr = p.attrib.get("start")
        if start_attr:
            # Use explicit start time from the MPD
            start = parse_iso_duration(start_attr)
            source = "explicit"  # Mark this as explicitly defined
        else:
            # Derive start time from the end of the previous period
            start = current_start
            source = "derived"  # Mark this as derived/calculated

        # Parse period duration (may be None if not specified)
        duration = parse_iso_duration(p.attrib.get("duration"))
        
        # Calculate end time if duration is available
        end = start + duration if duration else None
        
        # Update running start time for next period (if duration known)
        if duration:
            current_start = end

        # Store period timeline information
        timeline.append({
            "index": idx,           # Period sequence number
            "start": start,         # Period start time
            "duration": duration,   # Period duration (may be None)
            "end": end,             # Period end time (may be None)
            "source": source        # Whether start was explicit or derived
        })

    return timeline
