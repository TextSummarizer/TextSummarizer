from django.conf.urls import url
import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^documents/$', views.DocumentList.as_view()),
    url(r'^document/(?P<pk>[0-9]+)/$', views.DocumentDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
