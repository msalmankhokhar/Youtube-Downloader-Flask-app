from urllib.parse import urlparse, parse_qs
from pytubefix import YouTube, Stream
import re

sample_link = "https://www.youtube.com/watch?v=w330WRDgpKs"

def is_valid_youtube_url(url: str) -> bool:
    standard_pattern = re.compile(r'^https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+')
    mobile_pattern = re.compile(r'^https?://youtu\.be/[\w-]+')
    shorts_mobile_pattern = re.compile(r'^https?://(?:www\.)?youtube\.com/shorts/[\w-]+')
    return bool(standard_pattern.match(url) or mobile_pattern.match(url) or shorts_mobile_pattern.match(url))

def seconds_to_duration(seconds: int):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}"

def get_thumbnail_url(video_link: str):
    parsed_url = urlparse(video_link)
    params = parse_qs(parsed_url.query)
    video_id = params.get("v")[0]
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    

if __name__ == "__main__":
    v = YouTube(sample_link)
    print(v.embed_url)