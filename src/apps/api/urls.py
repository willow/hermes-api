from django.conf.urls import url
from src.apps.api.resources.agreement.views.agreement import agreement_create_view, agreement_update_view, \
  agreement_artifact_view
from src.apps.api.resources.user.views.user import user_view

urlpatterns = [
  url(r'^users/$', user_view),
  url(r'^agreements/(?P<agreement_id>\w+)/artifacts/(?P<artifact_id>\w+)/$', agreement_artifact_view),
  url(r'^agreements/$', agreement_create_view),
  url(r'^agreements/(?P<agreement_id>\w+)/$', agreement_update_view),
]
