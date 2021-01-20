from django.conf import settings
from rest_framework import pagination
from rest_framework.response import Response


class Pagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )
