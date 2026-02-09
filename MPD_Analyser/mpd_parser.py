# mpd_parser.py
import xml.etree.ElementTree as ET

# DASH namespace definition for XML parsing
# This namespace is used to query DASH-specific elements in the MPD XML
ns = {"dash": "urn:mpeg:dash:schema:mpd:2011"}

# Loads and parses an MPD (Media Presentation Description) XML file
# Returns the root element and namespace dictionary for XPath queries
def load_mpd(path):
    # Parse the XML file
    tree = ET.parse(path)
    
    # Get the root element (typically <MPD>)
    root = tree.getroot()
    
    # Return both root element and namespace for use in XPath queries
    return root, ns