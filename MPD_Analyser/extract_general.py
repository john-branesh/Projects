# extract_general.py
from datetime import timedelta
from utils import parse_iso_duration, format_timedelta

# Extracts general MPD characteristics and metadata
# Includes MPD type, profiles, buffer settings, period information, and ad signaling
def extract_general_capabilities(root, ns):
    # Initialize list to store capability rows (category, criteria, value)
    rows = []

    # Find all Period elements for analysis
    periods = root.findall("dash:Period", ns)

    # Extract MPD type (static for VOD, dynamic for live streaming)
    # Default to 'static' if not specified
    mpd_type = root.attrib.get("type", "static").capitalize()
    rows.append(("General", "MPD Type", mpd_type))

    # Extract DASH profiles (defines conformance and feature set)
    # e.g., "urn:mpeg:dash:profile:isoff-live:2011"
    profiles = root.attrib.get("profiles")
    rows.append((
        "General",
        "MPD Profiles",
        profiles if profiles else "Not specified"
    ))

    # Extract minimum buffer time (amount of content that must be buffered before playback)
    min_buffer = root.attrib.get("minBufferTime")
    rows.append((
        "General",
        "Minimum Buffer Time",
        format_timedelta(parse_iso_duration(min_buffer)) if min_buffer else "Not specified"
    ))

    # Extract availability start time (anchor time for live streams)
    # Used to calculate segment availability in dynamic presentations
    availability_start = root.attrib.get("availabilityStartTime")
    rows.append((
        "General",
        "Availability Start Time",
        availability_start if availability_start else "Not specified"
    ))

    # Extract time shift buffer depth (how far back users can seek in live content)
    # Only applicable for dynamic (live) presentations
    tsbd = root.attrib.get("timeShiftBufferDepth")

    # Report time shift buffer only for live/dynamic content
    if mpd_type.lower() == "dynamic":
        rows.append((
            "General",
            "Time Shift Buffer Depth",
            format_timedelta(parse_iso_duration(tsbd)) if tsbd else "Not specified"
        ))
    else:
        # VOD content doesn't need time shift buffer
        rows.append((
            "General",
            "Time Shift Buffer Depth",
            "Not applicable (VOD)"
        ))

    # Count periods (MPDs can have multiple periods for ads, chapters, etc.)
    rows.append(("General", "Number of Periods", str(len(periods))))
    rows.append(("General", "Multi-Period Content", "Yes" if len(periods) > 1 else "No"))

    # Calculate total playtime by summing all period durations
    # This represents the actual content duration
    total = timedelta()  # Accumulated total duration
    known = False       # Track if any duration information was found

    # Sum up durations from all periods
    for p in periods:
        dur = parse_iso_duration(p.attrib.get("duration"))
        if dur:
            total += dur
            known = True  # At least one duration was specified

    rows.append((
        "General",
        "Total Playtime",
        format_timedelta(total) if known else "Not specified in MPD"
    ))

    # Calculate the maximum period end time (structural analysis)
    # This represents the latest end time across all periods
    max_period_end = None          # Track the maximum end time found
    current_start = timedelta()    # Running start time for periods without explicit start

    # Iterate through periods to find the maximum end time
    for p in periods:
        # Get start time (explicit or derived from previous period)
        start_attr = p.attrib.get("start")
        start = parse_iso_duration(start_attr) if start_attr else current_start

        # Calculate end time if duration is available
        duration = parse_iso_duration(p.attrib.get("duration"))
        if duration:
            end = start + duration
            current_start = end  # Update running start for next period

            # Track the maximum end time across all periods
            if max_period_end is None or end > max_period_end:
                max_period_end = end

    rows.append((
        "General",
        "Max Period End Time",
        format_timedelta(max_period_end) if max_period_end else "Not specified in MPD"
    ))

    # Detect ad signaling mechanisms in the MPD
    # Ads can be signaled via EventStreams or multiple periods
    has_event_stream = bool(root.findall(".//dash:EventStream", ns))  # SCTE-35 or similar events
    has_multi_period = len(periods) > 1  # Multiple periods often indicate ad breaks

    # Report ad signaling presence and type
    if has_event_stream or has_multi_period:
        rows.append(("General", "Ad Signaling Present", "Yes"))
        rows.append((
            "General",
            "Ad Marker Type",
            "Period-based" if has_multi_period else "EventStream"
        ))
    else:
        # No ad signaling detected
        rows.append(("General", "Ad Signaling Present", "No"))
        rows.append(("General", "Ad Marker Type", "Not specified"))

    return rows
