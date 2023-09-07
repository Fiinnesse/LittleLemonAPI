from rest_framework.pagination import PageNumberPagination, BasePagination


class MenuItemsSetPagination(PageNumberPagination,BasePagination):
    display_page_controls = True
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 4
    
    