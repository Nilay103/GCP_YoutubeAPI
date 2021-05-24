import datetime
from googleapiclient.discovery import build

from fampay.settings import SEARCH_KEY, API_KEY
from youtube.models import YouTubeVideo


def upload_youtube_metadata():
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    latest_published_date = YouTubeVideo.get_latest_published_date().strftime("%Y-%m-%dT%H:%M:%SZ")
    MAX_RESULTS = 50

    request = youtube.search().list(
        q=SEARCH_KEY, part='snippet',
        maxResults=MAX_RESULTS,
        publishedAfter=latest_published_date,
        order='date')
    response = request.execute()

    youtube_videos = []
    published_before = ''
    for video_obj in response['items']:
        snippet = video_obj['snippet']
        youtube_videos.append(YouTubeVideo(**{
            'title': snippet['title'],
            'description': snippet['description'],
            'published_date': snippet['publishTime'],
            'thumbnail_url': snippet['thumbnails']['high']['url']
        }))
        published_before = snippet['publishTime']

    while response.get('nextPageToken') and response['pageInfo']['resultsPerPage'] == MAX_RESULTS:
        request = youtube.search().list(
            q=SEARCH_KEY, part='snippet',
            maxResults=MAX_RESULTS,
            publishedBefore=published_before,
            order='date')
        response = request.execute()
        for video_obj in response['items']:
            snippet = video_obj['snippet']
            youtube_videos.append(YouTubeVideo(**{
                'title': snippet['title'],
                'description': snippet['description'],
                'published_date': snippet['publishTime'],
                'thumbnail_url': snippet['thumbnails']['high']['url']
            }))
            published_before = snippet['publishTime']

    youtube_videos.reverse()
    YouTubeVideo.objects.bulk_create(youtube_videos, batch_size=500)
    return
