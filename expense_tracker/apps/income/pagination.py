from rest_framework.pagination import PageNumberPagination


class IncomePaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page"
    max_page_size = 10000
