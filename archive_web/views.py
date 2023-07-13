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
    page = Page.objects.create(url=url)
    crawl_task = CrawlTask.objects.create(page=page, config=data)
    crawl.delay(crawl_task.id, url, data)
    return JsonResponse({'status': 'success', 'id': page.id})


def get(request):
    _url = request.GET.get('url')
    url = base64.b64decode(_url.encode()).decode()
    page = Page.objects.filter(url=url).order_by('-id')
    if not page:
        return JsonResponse({'status': 'error', 'message': 'Not Found'})
    page = page.first()
    if not page.crawl_task.crawled_at:
        return JsonResponse({'status': 'error', 'message': 'Waiting...'})
    return JsonResponse({
        'status': 'success',
        'id': page.id,
        'url': page.url,
        'title': page.title,
        'images': page.images,
        'pdfs': page.pdfs,
    })
