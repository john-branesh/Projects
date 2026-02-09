# main.py
from pathlib import Path
from mpd_parser import load_mpd
from extract_general import extract_general_capabilities
from extract_periods import extract_period_timeline
from formatter import format_table, format_period_timeline
from extract_video import extract_video_capabilities
from extract_audio import extract_audio_capabilities
from extract_subtitles import extract_subtitle_capabilities
from extract_drm import extract_drm_capabilities


MPD_PATH = "/Users/jr/Downloads/house0fdragonss1e2dash.mpd"
OUTPUT_FILE = "mpd_capabilities.txt"

def main():
    root, ns = load_mpd(MPD_PATH)

    rows = []
    rows.extend(extract_general_capabilities(root, ns))
    rows.extend(extract_video_capabilities(root, ns))
    rows.extend(extract_audio_capabilities(root, ns))
    rows.extend(extract_subtitle_capabilities(root, ns))
    rows.extend(extract_drm_capabilities(root, ns))

    timeline = extract_period_timeline(root, ns)

    output = []
    output.append(format_table(rows))
    output.append(format_period_timeline(timeline))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print(f"Report written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
