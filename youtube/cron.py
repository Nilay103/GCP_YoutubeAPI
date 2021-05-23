from datetime import datetime
from googleapiclient.discovery import build

from youtube.models import YouTubeVideo


def my_cron_job(API_KEY, search_key):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    latest_published_date = YouTubeVideo.get_latest_published_date()
    request = youtube.search().list(
        q=search_key, part='snippet',
        maxResults=500,
        publishedAfter=latest_published_date,
        order='date')
    response = request.execute()
    youtube_videos = []
    for video_obj in response['items']:
        snippet = video_obj['snippet']
        youtube_videos.append(YouTubeVideo(**{
            'title': snippet['title'],
            'description': snippet['description'],
            'published_date': snippet['publishTime'],
            'thumbnail_url': snippet['thumbnails']['high']
        }))

    while response:
        request = youtube.search().list_next(request, response)
        response = request.execute()
        for video_obj in response['items']:
            snippet = video_obj['snippet']
            youtube_videos.append(YouTubeVideo(**{
                'title': snippet['title'],
                'description': snippet['description'],
                'published_date': snippet['publishTime'],
                'thumbnail_url': snippet['thumbnails']['high']
            }))

    YouTubeVideo.objects.bulk_create(youtube_videos)

    f = open(f"/home/nilay/Desktop/myfile{str(datetime.now())}.txt", "w")
    f.write(str(youtube_videos))
