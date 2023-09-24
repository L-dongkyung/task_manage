from rest_framework.pagination import CursorPagination


class TaskPagination(CursorPagination):
    page_size = 5
    ordering = 'create_at'
