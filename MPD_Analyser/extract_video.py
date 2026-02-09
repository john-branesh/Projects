# extract_video.py

# Extracts video-related capabilities from an MPD (Media Presentation Description) document
# Analyzes video tracks for codecs, resolutions, bitrates, and HDR support
def extract_video_capabilities(root, ns):
    # Initialize list to store capability rows (category, criteria, value)
    rows = []

    # Find all AdaptationSets with video content type
    video_sets = root.findall(".//dash:AdaptationSet[@contentType='video']", ns)

    # If no video tracks found, report and exit early
    if not video_sets:
        rows.append(("Video", "Video Tracks Present", "No"))
        return rows

    # Video tracks exist
    rows.append(("Video", "Video Tracks Present", "Yes"))

    # Initialize data structures to collect video properties
    codecs = set()           # Unique video codecs found
    resolutions = []         # List of (width, height) tuples
    bitrates = []           # List of bitrate values in bps

    # Initialize HDR detection flags (checked across all representations)
    hdr_present = False     # Whether any HDR content is detected
    hdr_types = set()       # Specific HDR types identified

    # Iterate through all video AdaptationSets
    for aset in video_sets:
        # Iterate through all Representations within each AdaptationSet
        for rep in aset.findall("dash:Representation", ns):
            # Extract codec information from representation
            codec = rep.attrib.get("codecs")
            if codec:
                codecs.add(codec)

                # Check if codec indicates Dolby Vision HDR
                if "dvhe" in codec.lower():
                    hdr_present = True
                    hdr_types.add("Dolby Vision")

            # Extract resolution (width x height)
            width = rep.attrib.get("width")
            height = rep.attrib.get("height")
            if width and height:
                resolutions.append((int(width), int(height)))

            # Extract bitrate (bandwidth in bits per second)
            bw = rep.attrib.get("bandwidth")
            if bw:
                bitrates.append(int(bw))

            # Check for HDR via transfer characteristics attribute
            # tc="16" indicates PQ (Perceptual Quantizer) used in HDR10
            # tc="18" indicates HLG (Hybrid Log-Gamma)
            tc = rep.attrib.get("transferCharacteristics")
            if tc == "16":
                hdr_present = True
                hdr_types.add("PQ (HDR10)")
            elif tc == "18":
                hdr_present = True
                hdr_types.add("HLG")

    # Add HDR capability rows
    rows.append((
        "Video",
        "HDR Present",
        "Yes" if hdr_present else "No"
    ))

    rows.append((
        "Video",
        "HDR Type(s)",
        ", ".join(sorted(hdr_types)) if hdr_types else "Not applicable"
    ))

    # Add video codec information
    rows.append(("Video", "Video Codec(s)", ", ".join(sorted(codecs)) if codecs else "Not specified"))

    # Process resolution data if available
    if resolutions:
        # Find maximum resolution by total pixel count (width × height)
        max_res = max(resolutions, key=lambda x: x[0] * x[1])
        # Find minimum resolution by total pixel count
        min_res = min(resolutions, key=lambda x: x[0] * x[1])

        rows.append(("Video", "Max Resolution", f"{max_res[0]}×{max_res[1]}"))
        rows.append(("Video", "Min Resolution", f"{min_res[0]}×{min_res[1]}"))

        # Check availability of common resolution tiers based on height
        rows.append(("Video", "UHD Available (≥2160p)", "Yes" if max_res[1] >= 2160 else "No"))
        rows.append(("Video", "FHD Available (≥1080p)", "Yes" if max_res[1] >= 1080 else "No"))
        rows.append(("Video", "HD Available (≥720p)", "Yes" if max_res[1] >= 720 else "No"))

    # Process bitrate data if available
    if bitrates:
        # Convert bitrates from bps to kbps for readability
        rows.append(("Video", "Max Video Bitrate", f"{max(bitrates)//1000} kbps"))
        rows.append(("Video", "Min Video Bitrate", f"{min(bitrates)//1000} kbps"))
        # Check if multiple bitrate options exist (adaptive bitrate streaming)
        rows.append((
            "Video",
            "Multiple Bitrate Ladder Present",
            "Yes" if len(set(bitrates)) > 1 else "No"
        ))

    return rows
