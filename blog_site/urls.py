from django.urls import path, include
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from .views import article_search

urlpatterns = [
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/",article_search, name="article_search" ),
    # path("pages/", include(wagtail_urls)),
    path("", include(wagtail_urls)),
]
