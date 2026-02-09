# extract_audio.py

# Extracts audio-related capabilities from an MPD (Media Presentation Description) document
# Analyzes audio tracks for codecs, languages, bitrates, and surround sound support
def extract_audio_capabilities(root, ns):
    # Initialize list to store capability rows (category, criteria, value)
    rows = []

    # Find all AdaptationSets with audio content type
    audio_sets = root.findall(
        ".//dash:AdaptationSet[@contentType='audio']", ns
    )

    # If no audio tracks found, report and exit early
    if not audio_sets:
        rows.append(("Audio", "Audio Tracks Present", "No"))
        return rows

    # Audio tracks exist
    rows.append(("Audio", "Audio Tracks Present", "Yes"))

    # Initialize data structures to collect audio properties
    codecs = set()      # Unique audio codecs found
    languages = set()   # Unique audio languages
    bitrates = []      # List of bitrate values in bps

    # Iterate through all audio AdaptationSets
    for aset in audio_sets:
        # Extract language code (e.g., 'en', 'es', 'fr')
        lang = aset.attrib.get("lang")
        if lang:
            languages.add(lang)

        # Iterate through all Representations within each AdaptationSet
        for rep in aset.findall("dash:Representation", ns):
            # Extract audio codec information (e.g., 'mp4a.40.2', 'ec-3', 'opus')
            codec = rep.attrib.get("codecs")
            if codec:
                codecs.add(codec)

            # Extract bitrate (bandwidth in bits per second)
            bw = rep.attrib.get("bandwidth")
            if bw:
                bitrates.append(int(bw))

    # Report all unique audio codecs found
    rows.append((
        "Audio",
        "Audio Codec(s)",
        ", ".join(sorted(codecs)) if codecs else "Not specified"
    ))

    # Report all unique audio languages available
    rows.append((
        "Audio",
        "Audio Languages",
        ", ".join(sorted(languages)) if languages else "Not specified"
    ))

    # Analyze bitrate data if available
    if bitrates:
        # Convert bitrates from bps to kbps for readability
        rows.append(("Audio", "Max Audio Bitrate", f"{max(bitrates)//1000} kbps"))
        rows.append(("Audio", "Min Audio Bitrate", f"{min(bitrates)//1000} kbps"))
        # Check if multiple bitrate options exist (adaptive bitrate streaming)
        rows.append((
            "Audio",
            "Multiple Audio Bitrates Present",
            "Yes" if len(set(bitrates)) > 1 else "No"
        ))
    else:
        # No bitrate information found in the MPD
        rows.append(("Audio", "Audio Bitrate Info", "Not specified"))

    # Count AdaptationSets (multiple sets may indicate different languages or audio descriptions)
    # Important for QA testing
    rows.append((
        "Audio",
        "Multiple Audio AdaptationSets",
        "Yes" if len(audio_sets) > 1 else "No"
    ))

    # Detect surround sound capability by checking for Dolby Digital codecs
    # ec-3 = Dolby Digital Plus (E-AC-3), ac-3 = Dolby Digital (AC-3)
    surround_codecs = [c for c in codecs if c.startswith("ec-3") or c.startswith("ac-3")]
    rows.append((
        "Audio",
        "Surround-capable Codec Present",
        "Yes" if surround_codecs else "No"
    ))

    return rows
