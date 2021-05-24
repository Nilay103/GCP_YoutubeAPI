from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView

from .models import YouTubeVideo
from .pagination import CustomPagination
from .serializers import YouTubeVideoSerializer
from fampay.settings import API_KEY

from googleapiclient.discovery import build


class YouTubeVideoViewSet(viewsets.ModelViewSet):
    queryset = YouTubeVideo.objects.all()
    serializer_class = YouTubeVideoSerializer
    pagination_class = CustomPagination
    http_method_names = ['get',]

    @action(methods=['GET'], detail=False, url_name='test')
    def test(self, request, pk=None):
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        MAX_RESULTS = 50

        latest_published_date = YouTubeVideo.get_latest_published_date().strftime("%Y-%m-%dT%H:%M:%SZ")
        request = youtube.search().list(
            q='coldplay', part='snippet',
            maxResults=MAX_RESULTS,
            publishedAfter=latest_published_date,
            order='date')
        response = request.execute()
        youtube_videos = []
        count = 0
        published_before = ''
        for video_obj in response['items']:
            snippet = video_obj['snippet']
            youtube_videos.append(YouTubeVideo(**{
                'title': snippet['title'],
                'description': snippet['description'],
                'published_date': snippet['publishTime'],
                'thumbnail_url': snippet['thumbnails']['high']
            }))
            count+=1
            published_before = snippet['publishTime']

        while response.get('nextPageToken') and response['pageInfo']['resultsPerPage'] == MAX_RESULTS:
            print(count)
            request = youtube.search().list(
                q='coldplay', part='snippet',
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
                count+=1
                published_before = snippet['publishTime']

        youtube_videos.reverse()
        YouTubeVideo.objects.bulk_create(youtube_videos, batch_size=500)
        return Response(YouTubeVideo.objects.values(), status=status.HTTP_200_OK)


class YouTubeVideoView(ListView):
    model = YouTubeVideo
    template_name = "videos_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(YouTubeVideoView, self).get_context_data(**kwargs) 
        queryset = YouTubeVideo.objects.all()

        page = self.request.GET.get('page')
        title = self.request.GET.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)

        paginator = Paginator(queryset, self.paginate_by)

        try:
            videos_list = paginator.page(page)
        except PageNotAnInteger:
            videos_list = paginator.page(1)
        except EmptyPage:
            videos_list = paginator.page(paginator.num_pages)

        context['videos_list'] = videos_list
        return context
