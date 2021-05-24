import datetime
from googleapiclient.discovery import build

from fampay.settings import SEARCH_KEY, API_KEY
from youtube.models import YouTubeVideo


MAX_RESULTS = 50


def get_response_is_valid(response):
    return response.get('nextPageToken') and response['pageInfo']['resultsPerPage'] == MAX_RESULTS


def get_youtube_api_response(youtube, latest_published_date, published_before):
    youtube_videos = []
    request = youtube.search().list(
        q=SEARCH_KEY,
        part='snippet',
        maxResults=MAX_RESULTS,
        publishedAfter=latest_published_date,
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

    return youtube_videos, published_before, get_response_is_valid()


def upload_youtube_metadata():
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    youtube_model_objs = []

    latest_published_date = YouTubeVideo.get_latest_published_date().strftime("%Y-%m-%dT%H:%M:%SZ")
    published_before = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    youtube_videos, published_before, is_valid = get_youtube_api_response(youtube, latest_published_date, published_before)
    youtube_model_objs += youtube_videos

    while is_valid:
        youtube_videos, published_before, is_valid = get_youtube_api_response(youtube, latest_published_date, published_before)
        youtube_model_objs += youtube_videos

    youtube_model_objs.reverse()
    YouTubeVideo.objects.bulk_create(youtube_model_objs, batch_size=500)
    return
