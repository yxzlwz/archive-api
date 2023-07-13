from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()

    images = models.JSONField(default=list)
    pdfs = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CrawlTask(models.Model):
    page = models.OneToOneField(
        Page,
        on_delete=models.CASCADE,
        related_name='crawl_task',
    )

    crawled_at = models.DateTimeField(blank=True, null=True)

    config = models.JSONField(default=dict)

    engine = models.CharField(max_length=31, blank=True, null=True)
    proxy = models.CharField(max_length=15, blank=True, null=True)
