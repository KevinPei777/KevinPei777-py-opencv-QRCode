__author__ = 'Pei'
from django.urls import re_path
from distinguish.views import DistinguishView, DistinguishQRCodeViw
app_name = 'distinguish'

urlpatterns = [
    re_path(r'^$', DistinguishView.as_view(), name='distinguish'),
    re_path(r'^post_pic', DistinguishQRCodeViw.as_view()),
]
