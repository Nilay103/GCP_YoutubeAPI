from rest_framework import viewsets
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView

from .filters import YouTubeVideoFilter
from .models import YouTubeVideo
from .pagination import CustomPagination
from .serializers import YouTubeVideoSerializer


class YouTubeVideoViewSet(viewsets.ModelViewSet):
    queryset = YouTubeVideo.objects.all().order_by('-id')
    serializer_class = YouTubeVideoSerializer
    pagination_class = CustomPagination
    http_method_names = ['get',]
    filterset_class = YouTubeVideoFilter

class YouTubeVideoView(ListView):
    model = YouTubeVideo
    template_name = "videos_list.html"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(YouTubeVideoView, self).get_context_data(**kwargs) 
        queryset = YouTubeVideo.objects.all().order_by('-id')

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
