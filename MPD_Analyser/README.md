# MPD Analyzer

## What is this?

This is a small Python tool that reads a **DASH MPD file** and extracts useful information from it in a **readable text format**.

MPD files are XML files and are usually very hard to understand by just opening them.  
This tool helps convert that XML into something easier to analyze.

---

## Why did I build this?

I built this as a **learning project** to understand:

- What information an MPD file actually contains
- Why MPDs have multiple periods
- How video, audio, subtitles, ads, and DRM are signaled
- How to analyze MPDs for **QA / device certification**

Instead of manually reading the MPD every time, this tool gives a clear summary.

---

## What does this tool do?

From the MPD file, it extracts:

### General / Timeline
- MPD type (static / dynamic)
- Total playtime (actual content duration)
- Max period end time (structural timeline)
- Number of periods
- Ad signaling (period-based or eventstream)
- Detailed period timeline (start, duration, end)

### Video
- Whether video tracks are present
- Video codec(s)
- Minimum and maximum resolution
- Min and max video bitrate
- HD / FHD / UHD availability
- Whether a bitrate ladder exists

### Audio
- Whether audio tracks are present
- Audio codec(s) (EC-3, AAC, etc.)
- Audio languages
- Min and max audio bitrate
- Multiple audio adaptation sets
- Surround-capable codec presence (derived)

### Subtitles
- Whether subtitles are present
- Subtitle languages
- Subtitle formats (TTML, WebVTT, etc.)
- Forced subtitles presence
- Subtitles across multiple periods

### DRM (Signaling only)
- Whether content is encrypted
- DRM systems present (Widevine, PlayReady, etc.)
- Multiple DRM systems or not
- Clear (unencrypted) tracks present or not

---

## What this tool does NOT do

- It does NOT play video
- It does NOT download content
- It does NOT tell actual playback quality
- It does NOT detect Widevine L1/L3
- It does NOT validate DRM licenses

This tool only analyzes **what the MPD advertises**, not what the device actually plays.

---

## Project structure

MPD_analyser/
├── main.py # Entry point
├── mpd_parser.py # MPD loading + namespace handling
├── utils.py # Common helper functions
│
├── extract_general.py # General info, playtime, ads
├── extract_periods.py # Period timeline extraction
├── extract_video.py # Video capability extraction
├── extract_audio.py # Audio capability extraction
├── extract_subtitles.py # Subtitle capability extraction
├── extract_drm.py # DRM signaling extraction
│
└── mpd_capabilities.txt # Output file

