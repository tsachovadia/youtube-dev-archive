# YouTube Developer Archive

A command-line tool to archive YouTube developer tutorials with metadata, transcripts, and organized documentation.

## Features

- Download video metadata and transcripts
- Generate organized README files for each video
- Extract templates and code references from video descriptions
- Easy-to-use terminal alias for quick archiving

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up the terminal alias:
   ```bash
   source scripts/setup_alias.sh
   ```

## Usage

Archive a YouTube video:
```bash
ytarchive "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Project Structure

```
videos/
├── video-title-1/
│   ├── README.md
│   ├── metadata.json
│   ├── transcript.txt
│   └── resources/
└── video-title-2/
    ├── README.md
    ├── metadata.json
    ├── transcript.txt
    └── resources/
```

Each video folder contains:
- **README.md**: Summary, key concepts, and templates from the video
- **metadata.json**: Video details, links, and technical information
- **transcript.txt**: Full video transcript
- **resources/**: Any extracted code snippets or templates