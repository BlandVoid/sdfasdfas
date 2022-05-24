from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "page": self.page.number,
                "previous": self.page.has_previous(),
                "next": self.page.has_next(),
                "results": data,
            }
        )
