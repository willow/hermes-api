from django.conf.urls import url
from src.apps.api.resources.user.views.user import user_view

urlpatterns = [
  url(r'^users/$', user_view),
]
