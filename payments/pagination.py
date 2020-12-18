from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
	page_size = 20
	page_size_query_param = 'page_size'
	max_page_size = 30
	offset_query_param = 'page'

	def get_paginated_response(self, data):
		return Response({
			'meta': {
				'next': self.get_next_link(),
				'previous': self.get_previous_link(),
				'length': self.page.paginator.count
			},
			'result': data,
			'status': True
		})