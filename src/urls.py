from django.conf.urls import include, url
from django.contrib import admin

from src.apps.api.urls import urlpatterns as api_urls

urlpatterns = [

]

# region Admin Urls
# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns.extend([
  url(r'^admin/', admin.site.urls),
])

# endregion

# region Lib Urls

# endregion

# region App Urls
urlpatterns.extend([
  url(r'^api/', include(api_urls)),
])
# endregion
