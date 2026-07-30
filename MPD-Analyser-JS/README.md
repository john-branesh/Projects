# MPD Analyser JS

A JavaScript CLI tool for parsing and analyzing DASH (Dynamic Adaptive Streaming over HTTP) Media Presentation Description (MPD) files.

This is a JS rebuild of my original [MPD Analyser](https://github.com/john-branesh/Projects/tree/main/MPD_Analyser) (Python), built to deepen my JavaScript/Node skills while working with a real-world file format.

## Overview

MPD Analyser JS reads a local DASH MPD file and extracts a clear, readable summary of what it signals — video quality options, audio tracks, subtitles, and DRM protection — instead of making you manually parse raw XML.

## Why did I build this?

As a learning project, to understand:
- What information an MPD file actually contains
- Why MPDs have multiple periods
- How video, audio, subtitles, ads, and DRM are signaled
- How to work with XML parsing and file I/O in Node.js

## Features (v1)

- **MPD Parsing**: Load and parse a local DASH MPD XML file, handling namespaces
- **General / Timeline**: MPD type (static/dynamic), total duration, number of periods, ad signaling
- **Video Extraction**: Codec(s), min/max resolution, min/max bitrate, HD/FHD/UHD availability
- **Audio Analysis**: Codec(s), languages, min/max bitrate, multiple adaptation sets
- **Subtitle Extraction**: Languages, formats, forced-subtitle detection
- **DRM Detection (signaling only)**: Which DRM systems are present (Widevine, PlayReady, etc.), clear vs encrypted tracks

## What this tool does NOT do

- Does not play video or download stream segments
- Does not tell you actual playback quality
- Does not detect Widevine L1/L3
- Does not validate DRM licenses

This tool only analyzes **what the MPD advertises**, not what a device actually plays.

## What is DASH/MPD?

**DASH** (Dynamic Adaptive Streaming over HTTP) is an adaptive bitrate streaming technology that lets a video player switch quality levels based on network conditions.

**MPD** (Media Presentation Description) is the XML manifest describing a DASH stream's available qualities, audio tracks, subtitles, and DRM protection.

## Installation

```bash
git clone <repository-url>
cd MPD_Analyser_JS
npm install
```

## Usage

```bash
node src/index.js ./sample-mpd/example.mpd
```

This prints a structured summary of the MPD to your terminal.

## Project Structure

```
MPD_Analyser_JS/
├── src/
│   ├── index.js            # CLI entry point
│   ├── parser.js            # MPD XML loading + namespace handling
│   ├── utils.js              # Shared helper functions
│   └── extractors/
│       ├── general.js       # General info, timeline, ad signaling
│       ├── periods.js       # Period timeline extraction
│       ├── video.js         # Video capability extraction
│       ├── audio.js         # Audio capability extraction
│       ├── subtitles.js     # Subtitle capability extraction
│       └── drm.js           # DRM signaling extraction
├── sample-mpd/
│   └── example.mpd          # Sample file for testing
├── package.json
└── README.md
```

## Requirements

- Node.js 16.0.0 or higher
- npm 7.0.0 or higher

## Dependencies

- [`fast-xml-parser`](https://www.npmjs.com/package/fast-xml-parser) — parses the MPD's XML into a JS object. Chosen over alternatives like `xml2js` for being actively maintained, having zero sub-dependencies, and simpler async-free usage.

## Example Output

```
=== General ===
Type: static
Total periods: 3
Total playtime: 1h 30m 15s
Ad signaling: period-based

=== Video ===
Codecs: avc1.640028, hvc1.1.6.L93.90
Resolution range: 1280x720 - 3840x2160
Bitrate range: 2,000,000 - 15,000,000 bps
Includes UHD: yes

=== Audio ===
Codecs: ec-3, aac
Languages: en, es
Bitrate range: 128,000 - 192,000 bps

=== Subtitles ===
Languages: en
Formats: vtt
Forced subtitles present: yes

=== DRM ===
Encrypted: yes
Systems: Widevine, PlayReady
Clear tracks present: no
```

## Roadmap (planned, not yet built)

- [ ] Fetch MPD from a remote URL (not just local files)
- [ ] Frame rate extraction for video tracks
- [ ] Audio channel count (stereo/surround) parsing
- [ ] DRM key ID and license URL extraction
- [ ] JSON output mode (for piping into other tools)
- [ ] Unit tests for each extractor
- [ ] CLI flags (`--video-only`, `--check-drm`, etc.)

## License

MIT

## Related Projects

- [MPD Analyser](https://github.com/john-branesh/Projects/tree/main/MPD_Analyser) — the original Python version

---

For more on DASH and MPD specifications, see the [DASH Industry Forum](https://dashif.org/).