__author__ = 'Pei'
from django.urls import re_path
from beautify.views import CodeBeautify, MakeNewCode
app_name = 'beautify'

urlpatterns = [
    re_path(r'^$', CodeBeautify.as_view(), name='beautify'),
    re_path(r'^new_code', MakeNewCode.as_view()),
]
