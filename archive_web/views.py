from datetime import timedelta

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet

from crawl.tasks import crawl

from .models import CrawlTask, Page
from .serializers import PageSerializer, BriefPageSerializer


class PageViewSet(ReadOnlyModelViewSet):
    queryset = Page.objects.exclude(crawl_task__crawled_at=None)
    serializer_class = PageSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['url', 'title']
    filterset_fields = ['url', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return BriefPageSerializer
        return PageSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if request.GET.get('url'):
            url = request.GET.get('url')
            url = url.split('?')[0]
            queryset = queryset.filter(url__startswith=url)
        elif request.GET.get('title'):
            title = request.GET.get('title')
            queryset = queryset.filter(title__contains=title)
        queryset = queryset.order_by('-id')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        url = data.pop('url')
        _page = Page.objects.filter(url=url, crawl_task__crawled_at=None)
        if _page.exists():
            _page = _page.first()
            if _page.created_at + timedelta(minutes=1) < timezone.now():
                _page.delete()
            else:
                return Response({
                    'status': 'error',
                    'message': 'Same url crawling...'
                })
        page = Page.objects.create(url=url)
        crawl_task = CrawlTask.objects.create(page=page, config=data)
        crawl.delay(crawl_task.id, url, data)
        return Response({'status': 'success', 'id': page.id})

    @action(detail=True, methods=['get'], url_path='check')
    def check(self, request, *args, **kwargs):
        page = self.get_object()
        if page.crawl_task.crawled_at:
            return Response({'status': 'success'})
        return Response({})
