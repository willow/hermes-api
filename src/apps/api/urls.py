from django.conf.urls import url

from src.apps.api.resources.agreement.views.agreement import agreement_create_view, agreement_update_view
from src.apps.api.resources.asset.views.asset import asset_view
from src.apps.api.resources.search.views.search import federated_search_view, advanced_search_view
from src.apps.api.resources.smart_view.views.smart_view import smart_view_create_view
from src.apps.api.resources.smart_view.views.smart_view import smart_view_update_view
from src.apps.api.resources.user.views.user import user_view

urlpatterns = [
  url(r'^users/$', user_view),
  url(r'^assets/(?P<asset_id>\w+)/$', asset_view),
  url(r'^agreements/$', agreement_create_view),
  url(r'^agreements/(?P<agreement_id>\w+)/$', agreement_update_view),
  url(r'^search/federated/$', federated_search_view),
  url(r'^search/agreements/$', advanced_search_view),
  url(r'^smart-views/$', smart_view_create_view),
  url(r'^smart-views/(?P<smart_view_id>\w+)/$', smart_view_update_view),
]
