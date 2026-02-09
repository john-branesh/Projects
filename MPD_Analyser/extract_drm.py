# extract_drm.py

# Extracts DRM (Digital Rights Management) and encryption information from an MPD
# Identifies DRM systems (Widevine, PlayReady, FairPlay) and encryption status
def extract_drm_capabilities(root, ns):
    # Initialize list to store capability rows (category, criteria, value)
    rows = []

    # Find all ContentProtection elements (both with and without namespace prefix)
    # ContentProtection indicates encrypted content and specifies DRM systems
    content_protections = (
        root.findall(".//dash:ContentProtection", ns)
        + root.findall(".//ContentProtection")
    )

    # If no ContentProtection elements found, content is unencrypted
    if not content_protections:
        rows.append(("DRM", "Content Encrypted", "No"))
        rows.append(("DRM", "DRM Systems Present", "None"))
        return rows

    # ContentProtection elements exist, content is encrypted
    rows.append(("DRM", "Content Encrypted", "Yes"))

    # Set to store unique DRM systems found
    drm_systems = set()

    # Map of DRM system UUIDs to friendly names
    # These UUIDs are standardized identifiers for each DRM system
    DRM_UUID_MAP = {
        "edef8ba9-79d6-4ace-a3c8-27dcd51d21ed": "Widevine",    # Google Widevine
        "9a04f079-9840-4286-ab92-e65be0885f95": "PlayReady",   # Microsoft PlayReady
        "94ce86fb-07ff-4f43-adb8-93d2fa968ca2": "FairPlay",    # Apple FairPlay
    }

    # Check each ContentProtection element for known DRM system UUIDs
    for cp in content_protections:
        # Extract the schemeIdUri attribute (contains DRM system UUID)
        scheme = cp.attrib.get("schemeIdUri", "").lower()
        
        # Match against known DRM system UUIDs
        for uuid, name in DRM_UUID_MAP.items():
            if uuid in scheme:
                drm_systems.add(name)

    # Report identified DRM systems
    rows.append((
        "DRM",
        "DRM Systems Present",
        ", ".join(sorted(drm_systems)) if drm_systems else "Unknown / Custom"
    ))

    # Check if multi-DRM is implemented (multiple DRM systems for cross-platform support)
    rows.append((
        "DRM",
        "Multiple DRM Systems Present",
        "Yes" if len(drm_systems) > 1 else "No"
    ))

    # Check if any AdaptationSets lack ContentProtection (clear/unencrypted tracks)
    # Some MPDs mix encrypted and unencrypted tracks
    clear_tracks = False
    
    # Iterate through all AdaptationSets
    for aset in root.findall(".//dash:AdaptationSet", ns):
        # If this AdaptationSet has no ContentProtection elements, it's unencrypted
        if not (
            aset.findall("dash:ContentProtection", ns)
            or aset.findall("ContentProtection")
        ):
            clear_tracks = True
            break  # Found at least one clear track

    # Report presence of clear (unencrypted) tracks
    rows.append((
        "DRM",
        "Clear (Unencrypted) Tracks Present",
        "Yes" if clear_tracks else "No"
    ))

    return rows
