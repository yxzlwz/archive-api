import base64
import json
from django.shortcuts import HttpResponse, HttpResponseRedirect
from crawl.tasks import crawl
from .models import Page, CrawlTask


def JsonResponse(data):
    return HttpResponse(json.dumps(data), content_type='application/json')


def create(request):
    data = json.loads(request.body)
    print(data)
    url = data.pop('url')
    if Page.objects.filter(url=url, crawl_task__crawled_at=None).exists():
        return JsonResponse({
            'status': 'error',
            'message': 'Same url crawling...'
        })
    page = Page.objects.create(url=url)
    crawl_task = CrawlTask.objects.create(page=page, config=data)
    crawl.delay(crawl_task.id, url, data)
    return JsonResponse({'status': 'success', 'id': page.id})


def get(request):
    url = request.GET.get('url')
    page = Page.objects.filter(url=url).order_by('-id')
    if not page:
        return JsonResponse({'status': 'error', 'message': 'Not Found'})
    page = page.first()
    if not page.crawl_task.crawled_at:
        return JsonResponse({'status': 'error', 'message': 'Crawling...'})
    return JsonResponse({
        'status': 'success',
        'id': page.id,
        'url': page.url,
        'title': page.title,
        'images': page.images,
        'pdfs': page.pdfs,
    })


def search(request):
    key = request.GET.get('key')
    by_url = Page.objects.filter(url__startswith=key)[:10]
    by_title = Page.objects.filter(title__contains=key)[:10]
    by_url = [{'id': i.id, 'title': i.title, 'url': i.url} for i in by_url]
    by_title = [{'id': i.id, 'title': i.title, 'url': i.url} for i in by_title]
    return JsonResponse({
        'status': 'success',
        'by_url': by_url,
        'by_title': by_title,
    })
