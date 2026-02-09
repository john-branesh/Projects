# formatter.py
from utils import format_timedelta

# Formats capability data into a markdown-style table with columns for serial number,
# capability category, criteria, and availability status in the MPD
def format_table(rows):
    lines = []
    lines.append("| S.No | Capability Category | Capability / Criteria | Available in MPD |")
    lines.append("|-----:|---------------------|----------------------|------------------|")

    for i, (cat, crit, val) in enumerate(rows, start=1):
        lines.append(f"| {i:<4} | {cat:<19} | {crit:<20} | {val} |")

    return "\n".join(lines)


# Formats period timeline information into a readable text display
# showing start time, duration, and end time for each period in the MPD
def format_period_timeline(timeline):
    lines = ["", "===== PERIOD TIMELINE =====", ""]

    for p in timeline:
        lines.append(f"Period {p['index']}:")
        lines.append(f"  Start    : {format_timedelta(p['start'])} ({p['source']})")
        lines.append(f"  Duration : {format_timedelta(p['duration']) if p['duration'] else 'Not specified'}")
        lines.append(f"  End      : {format_timedelta(p['end']) if p['end'] else 'Not determinable'}")
        lines.append("")

    return "\n".join(lines)
