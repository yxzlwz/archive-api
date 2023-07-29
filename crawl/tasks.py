from celery import shared_task
from django.utils import timezone

from archive_web.models import CrawlTask

from .selenium_chrome import SeleniumChrome
from .utils import md5


@shared_task
def crawl(task_id, url, config):
    task = CrawlTask.objects.get(id=task_id)
    page = task.page

    filename = f'{md5(url)}_{int(page.created_at.timestamp() * 1000)}'
    engine = SeleniumChrome()
    data, deatil = engine.archive(url, filename, config)

    task.crawled_at = timezone.now()
    task.detail = deatil
    task.save()

    page.title = data['title']
    page.images = data['images']
    page.pdfs = data['pdfs']
    page.save()
