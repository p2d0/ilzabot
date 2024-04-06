import requests
import random
from googleapiclient.discovery import build
from pytube import YouTube
import os

API_KEY = "AIzaSyAHOEcrfGXrQra5sWF9HBvYVHihH35hdj0"

def get_youtube_videos_under_30_seconds():
    youtube_api_service_name = "youtube"
    youtube_api_version = "v3"

    youtube = build(youtube_api_service_name, youtube_api_version, developerKey=API_KEY)

    search_request = youtube.search().list(
        part="snippet",
        maxResults=50,
        q="trailer",
        type="video",
        videoDuration="short",
        order="viewCount"
    )

    search_response = search_request.execute()
    video_ids = [video["id"]["videoId"] for video in search_response["items"]]

    return video_ids

def download_random_short_video(video_id):
    youtube = YouTube(f"https://www.youtube.com/watch?v={video_id}", on_progress_callback=None, on_complete_callback=None)
    video = youtube.streams.get_by_resolution("720p")
    video_title = video.title

    # Create the "videos" folder if it doesn't exist
    if not os.path.exists("videos"):
        os.makedirs("videos")

    # Save the video in the "videos" folder
    video.download("videos")

    return os.path.join("videos", video.default_filename), video_title

def download_random_short():
    video_ids = get_youtube_videos_under_30_seconds()
    random_video_id = random.choice(video_ids)
    input_video_file, video_title = download_random_short_video(random_video_id)
    return input_video_file;

def main():
    video_ids = get_youtube_videos_under_30_seconds()
    random_video_id = random.choice(video_ids)

    print(random_video_id);

    input_video_file, video_title = download_random_short_video(random_video_id)
    print(f"Downloaded video: {input_video_file}")

if __name__ == "__main__":
    main()
