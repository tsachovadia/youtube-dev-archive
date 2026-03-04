# youtube-dev-archive

CLI tool to archive YouTube developer tutorials with metadata, transcripts, and resources.

## Features

- **Metadata extraction** -- pulls title, channel, duration, upload date, and description via `yt-dlp`
- **Transcript download** -- fetches full video transcripts using `youtube-transcript-api`
- **Resource extraction** -- parses descriptions for templates, code links, and related URLs
- **Organized output** -- creates a dedicated folder per video with `metadata.json`, `transcript.txt`, and a generated `README.md`

## Requirements

- Python 3.x
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)

## Setup

```bash
pip install -r requirements.txt
source scripts/setup_alias.sh
```

## Usage

```bash
ytarchive "https://youtube.com/watch?v=VIDEO_ID"
```

Each archived video produces a folder under `videos/`:

```
videos/
└── video-title/
    ├── README.md        # auto-generated summary
    ├── metadata.json    # full video metadata
    ├── transcript.txt   # complete transcript
    └── resources/       # extracted code snippets & templates
```

## License

[MIT](LICENSE)
