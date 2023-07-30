from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from archive_web import views

router = DefaultRouter()
router.register(r'page', views.PageViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
]
