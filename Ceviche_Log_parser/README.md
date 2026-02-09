# Log Processor Utility

This repository contains a simple Python utility used to assist with
log analysis during device and application validation activities.

The script was written to reduce manual effort when analyzing large
volumes of log files by filtering relevant entries based on configurable
keywords.

## What the Script Does

- Reads multiple log files from a directory
- Filters log lines using a set of parent keywords
- Performs a secondary filtering using child keywords
- Organizes extracted logs into structured output folders

## Why This Exists

During large-scale testing, logs often contain thousands of lines.
Manually searching for errors or specific events is inefficient.

This script helps by:
- Automating keyword-based log extraction
- Reducing repetitive manual searches
- Organizing outputs for faster debugging

## Directory Structure

Projects/
│
├── LOGS/ # Input log files (.txt)
├── output_files/ # Generated output files
│ └── <keyword>/
│ ├── <keyword>output.txt
│ └── <keyword><child>_output.txt
│
├── log_processor.py
└── README.md

## How to Use

1. Place log files inside the `LOGS` directory
2. Configure keywords in the script:
   ```python
   initial_keywords = ["ERROR", "WARN"]
   additional_keywords = ["timeout", "buffer"]
   
Run the script:
python log_processor.py

Notes
This is a generic utility script
No proprietary data or internal systems are included
Designed as a lightweight helper for QA and validation workflows