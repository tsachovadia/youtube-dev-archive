#!/usr/bin/env python3
"""
YouTube Developer Archive Tool
Archives YouTube videos with metadata, transcripts, and documentation.
"""

import os
import sys
import json
import re
import argparse
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import subprocess
import requests
from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id(url):
    """Extract video ID from YouTube URL."""
    parsed = urlparse(url)
    
    if parsed.hostname in ['youtu.be']:
        return parsed.path[1:]
    elif parsed.hostname in ['youtube.com', 'www.youtube.com']:
        if 'v' in parse_qs(parsed.query):
            return parse_qs(parsed.query)['v'][0]
    
    return None


def get_video_metadata(video_id):
    """Get video metadata using yt-dlp."""
    try:
        cmd = ['yt-dlp', '--dump-json', '--no-download', f'https://www.youtube.com/watch?v={video_id}']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error getting metadata: {e}")
        return None


def get_transcript(video_id):
    """Get video transcript."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join([item['text'] for item in transcript_list])
    except Exception as e:
        print(f"Error getting transcript: {e}")
        return None


def sanitize_filename(filename):
    """Sanitize filename for filesystem."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with hyphens and convert to lowercase
    filename = re.sub(r'\s+', '-', filename).lower()
    # Remove multiple consecutive hyphens
    filename = re.sub(r'-+', '-', filename)
    # Remove leading/trailing hyphens
    filename = filename.strip('-')
    # Limit length
    return filename[:100]


def extract_templates_from_description(description):
    """Extract templates, code snippets, and resources from description."""
    templates = []
    
    # Look for common patterns
    patterns = [
        r'template[s]?[:\s]+(.+)',
        r'code[:\s]+(.+)',
        r'github[:\s]+(.+)',
        r'resource[s]?[:\s]+(.+)',
        r'link[s]?[:\s]+(.+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, description, re.IGNORECASE | re.MULTILINE)
        templates.extend(matches)
    
    # Extract URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, description)
    
    return {
        'templates': templates,
        'urls': urls
    }


def create_video_readme(metadata, transcript, video_folder):
    """Create a README file for the video."""
    title = metadata.get('title', 'Unknown Title')
    description = metadata.get('description', '')
    duration = metadata.get('duration', 0)
    upload_date = metadata.get('upload_date', '')
    uploader = metadata.get('uploader', '')
    
    # Extract templates and resources
    resources = extract_templates_from_description(description)
    
    # Format upload date
    if upload_date:
        try:
            date_obj = datetime.strptime(upload_date, '%Y%m%d')
            formatted_date = date_obj.strftime('%B %d, %Y')
        except:
            formatted_date = upload_date
    else:
        formatted_date = 'Unknown'
    
    # Format duration
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    
    if hours > 0:
        duration_str = f"{hours}h {minutes}m {seconds}s"
    else:
        duration_str = f"{minutes}m {seconds}s"
    
    readme_content = f"""# {title}

**Channel:** {uploader}  
**Duration:** {duration_str}  
**Upload Date:** {formatted_date}  
**Video URL:** {metadata.get('webpage_url', '')}

## Summary

{description[:500]}{'...' if len(description) > 500 else ''}

## Key Concepts

<!-- Add key concepts and takeaways from the video here -->

## Templates & Resources

"""
    
    if resources['templates']:
        readme_content += "### Templates\n"
        for template in resources['templates'][:5]:  # Limit to 5
            readme_content += f"- {template.strip()}\n"
        readme_content += "\n"
    
    if resources['urls']:
        readme_content += "### Links\n"
        for url in resources['urls'][:10]:  # Limit to 10
            readme_content += f"- {url}\n"
        readme_content += "\n"
    
    readme_content += """## Code Snippets

<!-- Add important code snippets from the video here -->

## Notes

<!-- Add your personal notes and insights here -->

## Related Videos

<!-- Link to related videos in your archive -->
"""
    
    readme_path = os.path.join(video_folder, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)


def archive_video(url):
    """Main function to archive a YouTube video."""
    video_id = get_video_id(url)
    if not video_id:
        print("Error: Invalid YouTube URL")
        return False
    
    print(f"Archiving video: {video_id}")
    
    # Get metadata
    metadata = get_video_metadata(video_id)
    if not metadata:
        return False
    
    # Create video folder
    title = metadata.get('title', f'video-{video_id}')
    folder_name = sanitize_filename(title)
    video_folder = os.path.join('videos', folder_name)
    
    os.makedirs(video_folder, exist_ok=True)
    os.makedirs(os.path.join(video_folder, 'resources'), exist_ok=True)
    
    # Save metadata
    metadata_path = os.path.join(video_folder, 'metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    # Get and save transcript
    transcript = get_transcript(video_id)
    if transcript:
        transcript_path = os.path.join(video_folder, 'transcript.txt')
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
    
    # Create README
    create_video_readme(metadata, transcript, video_folder)
    
    print(f"✅ Video archived successfully in: {video_folder}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Archive YouTube developer videos')
    parser.add_argument('url', help='YouTube video URL')
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    os.chdir(project_dir)
    
    success = archive_video(args.url)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()