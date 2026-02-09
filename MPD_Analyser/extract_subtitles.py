# extract_subtitles.py

# Extracts subtitle-related capabilities from an MPD (Media Presentation Description) document
# Analyzes subtitle tracks for languages, formats, forced subtitles, and multi-period presence
def extract_subtitle_capabilities(root, ns):
    # Initialize list to store capability rows (category, criteria, value)
    rows = []

    # Find all AdaptationSets with text content type (DASH subtitles are typically declared as text)
    # Note: Some implementations may also use contentType='application' for subtitles
    subtitle_sets = root.findall(
        ".//dash:AdaptationSet[@contentType='text']",
        ns
    )

    # If no subtitle tracks found, report and exit early
    if not subtitle_sets:
        rows.append(("Subtitles", "Subtitles Present", "No"))
        return rows

    # Subtitle tracks exist
    rows.append(("Subtitles", "Subtitles Present", "Yes"))

    # Initialize data structures to collect subtitle properties
    languages = set()          # Unique languages found in subtitle tracks
    formats = set()           # Unique subtitle formats/MIME types
    forced_present = False    # Whether forced subtitles exist (for foreign language dialogue)

    # Iterate through all subtitle AdaptationSets
    for aset in subtitle_sets:
        # Extract language code (e.g., 'en', 'es', 'fr')
        lang = aset.attrib.get("lang")
        if lang:
            languages.add(lang)

        # Check Role elements to identify forced subtitles
        # Forced subtitles display only for foreign language parts of the content
        for role in aset.findall("dash:Role", ns):
            if role.attrib.get("value", "").lower() == "forced":
                forced_present = True

        # Iterate through Representations to extract format details
        for rep in aset.findall("dash:Representation", ns):
            # Extract MIME type (e.g., 'application/ttml+xml', 'text/vtt')
            mime = aset.attrib.get("mimeType")
            if mime:
                formats.add(mime)

            # Extract codec attribute as it sometimes provides format hints
            codec = rep.attrib.get("codecs")
            if codec:
                formats.add(codec)

    # Add subtitle language information
    rows.append((
        "Subtitles",
        "Subtitle Languages",
        ", ".join(sorted(languages)) if languages else "Not specified"
    ))

    # Add subtitle format information
    rows.append((
        "Subtitles",
        "Subtitle Format(s)",
        ", ".join(sorted(formats)) if formats else "Not specified"
    ))

    # Add forced subtitles availability
    rows.append((
        "Subtitles",
        "Forced Subtitles Present",
        "Yes" if forced_present else "No"
    ))

    # Check if multiple subtitle AdaptationSets exist (multiple language/format options)
    rows.append((
        "Subtitles",
        "Multiple Subtitle AdaptationSets",
        "Yes" if len(subtitle_sets) > 1 else "No"
    ))

    # Analyze subtitle presence across multiple periods
    # (Multi-period MPDs can have different subtitle availability in each period)
    periods_with_subs = set()  # Track which period indices contain subtitles
    periods = root.findall("dash:Period", ns)

    # Check each period for subtitle AdaptationSets
    for idx, period in enumerate(periods):
        subs_in_period = period.findall(
            ".//dash:AdaptationSet[@contentType='text']",
            ns
        )
        # If this period has subtitles, record its index
        if subs_in_period:
            periods_with_subs.add(idx)

    # Report whether subtitles span multiple periods
    rows.append((
        "Subtitles",
        "Subtitles Across Multiple Periods",
        "Yes" if len(periods_with_subs) > 1 else "No"
    ))

    return rows
