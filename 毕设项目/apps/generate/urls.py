__author__ = 'Pei'
from django.urls import re_path
from generate.views import IndexView, UrlQRCodeView, PicQRCodeView, FileCodeView
from generate.views import TextCodeView, MakeUrlCodeView, MakePicCode, MakeFileCode
app_name = 'generate'
urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='index'),
    re_path(r'^url$', UrlQRCodeView.as_view(), name='url'),
    re_path(r'^pic$', PicQRCodeView.as_view(), name='pic'),
    re_path(r'^files$', FileCodeView.as_view(), name='files'),

    # 文本二维码
    re_path(r'^text_code', TextCodeView.as_view()),
    # url二维码
    re_path(r'^url_code', MakeUrlCodeView.as_view()),
    # 图片二维码
    re_path(r'^pic_code', MakePicCode.as_view()),
    # 文件二维码
    re_path(r'^file_code', MakeFileCode.as_view()),
]
