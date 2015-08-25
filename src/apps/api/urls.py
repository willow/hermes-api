from django.conf.urls import url
from src.apps.api.resources.agreement.views.agreement import agreement_view
from src.apps.api.resources.user.views.user import user_view

urlpatterns = [
  url(r'^users/$', user_view),
  url(r'^agreements/$', agreement_view),
]
