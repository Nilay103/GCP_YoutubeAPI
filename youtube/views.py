from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import YouTubeVideo
from .pagination import CustomPagination
from .serializers import YouTubeVideoSerializer

from datetime import datetime
from googleapiclient.discovery import build
from fampay.settings import API_KEY


""" class YouTubeVideoViewSet(APIView):
    queryset = YouTubeVideo.objects.all()
    serializer_class = YouTubeVideoSerializer
    pagination_class = CustomPagination
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'videos_list.html'

    @action(methods=['GET'], detail=False, url_name='test')
    def test(self, request, pk=None):
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        latest_published_date = YouTubeVideo.get_latest_published_date()
        # request = youtube.search().list(
        #     q=search_key, part='snippet',
        #     maxResults=500,
        #     publishedAfter=latest_published_date,
        #     order='date')
        # response = request.execute()
        a = YouTubeVideo(**{
            'title': 't',
            'description': 'd',
            'published_date': '2021-05-23T15:00:32Z',
            'thumbnail_url': 'u'
        })
        youtube_videos = [a]
        # for video_obj in response['items']:
        #     snippet = video_obj['snippet']
        #     youtube_videos.append(YouTubeVideo(**{
        #         'title': snippet['title'],
        #         'description': snippet['description'],
        #         'published_date': snippet['publishTime'],
        #         'thumbnail_url': snippet['thumbnails']['high']
        #     }))

        # while response:
        #     request = youtube.search().list_next(request, response)
        #     response = request.execute()
        #     for video_obj in response['items']:
        #         snippet = video_obj['snippet']
        #         youtube_videos.append(YouTubeVideo(**{
        #             'title': snippet['title'],
        #             'description': snippet['description'],
        #             'published_date': snippet['publishTime'],
        #             'thumbnail_url': snippet['thumbnails']['high']
        #         }))

        YouTubeVideo.objects.bulk_create(youtube_videos)

        f = open(f"/home/nilay/Desktop/myfile{str(datetime.now())}.txt", "w")
        f.write(str(youtube_videos))
        return Response(YouTubeVideo.objects.values(), status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return Response({'data': list(YouTubeVideo.objects.values())}, template_name='videos_list.html')
 """

class YouTubeVideoViewSet(viewsets.ModelViewSet):
    queryset = YouTubeVideo.objects.all()
    serializer_class = YouTubeVideoSerializer
    pagination_class = CustomPagination
    http_method_names = ['get',]


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView


class YouTubeVideoView(ListView):
    model = YouTubeVideo
    template_name = "videos_list.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(YouTubeVideoView, self).get_context_data(**kwargs) 
        queryset = YouTubeVideo.objects.all()
        paginator = Paginator(queryset, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            videos_list = paginator.page(page)
        except PageNotAnInteger:
            videos_list = paginator.page(1)
        except EmptyPage:
            videos_list = paginator.page(paginator.num_pages)
            
        context['videos_list'] = videos_list
        return context
