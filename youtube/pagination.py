from rest_framework import pagination

from fampay.settings import PAGE_SIZE


class CustomPagination(pagination.PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = PAGE_SIZE
    page_query_param = 'p'
