from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """
    Custom pagination class for API endpoints that:
    - Sets default page size to 10 items per page
    - Allows client to override page size via 'page_size' query parameter
    - Limits maximum page size to 50 items per page
    
    Usage:
        Add to ViewSet: pagination_class = StandardPagination
        Query params: ?page=1&page_size=20
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
