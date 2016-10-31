from django.conf.urls import include, url
from django.contrib import admin

from src.apps.api.urls import urlpatterns as api_urls

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^django-rq/', include('django_rq.urls')),
  url(r'^api/', include(api_urls)),
]
