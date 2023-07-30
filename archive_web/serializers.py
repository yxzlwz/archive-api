from rest_framework import serializers
from .models import Page, CrawlTask


class BriefPageSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()

    def get_cover(self, obj):
        return obj.images[0] if obj.images else None

    class Meta:
        model = Page
        fields = ('id', 'title', 'url', 'created_at', 'cover')
        read_only_fields = ('id', 'title', 'created_at', 'cover')


class CrawlTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrawlTask
        fields = ('id', 'config', 'crawled_at', 'detail')
        read_only_fields = ('id', 'config', 'crawled_at', 'detail')


class PageSerializer(serializers.ModelSerializer):
    crawl_task = CrawlTaskSerializer()

    class Meta:
        model = Page
        fields = ('id', 'title', 'url', 'images', 'pdfs', 'created_at',
                  'updated_at', 'crawl_task')
        read_only_fields = ('id', 'title', 'images', 'pdfs', 'created_at',
                            'updated_at', 'crawl_task')
