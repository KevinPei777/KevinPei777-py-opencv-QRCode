from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View
from django.utils.six import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import re
import qrcode
import base64
from io import BytesIO
import leancloud
# Create your views here.


# 主页视图
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


# 异步生成文本二维码
class TextCodeView(View):
    def post(self, request):
        text = request.POST['content']
        text = text.encode('utf8')
        img = qrcode.make(text)
        buf = BytesIO()
        img.save(buf)
        img_stream = buf.getvalue()
        result_img = base64.b64encode(img_stream)
        return JsonResponse({"msg": "测试成功", "image": bytes.decode(result_img, 'utf-8')})


# url二维码视图
class UrlQRCodeView(View):
    def get(self, request):
        return render(request, 'makeCode_url.html', {})


# 异步生成url二维码
class MakeUrlCodeView(View):
    def post(self, request):
        url = request.POST['url']
        result = re.match("^([hH][tT]{2}[pP]://|[hH][tT]{2}[pP][sS]://|[wW]{3}\.)(([A-Za-z0-9-~]+).)+([A-Za-z0-9-~\\/])+$", url)
        if result:
            if result.group()[:4] == 'www.':
                img = qrcode.make('http://'+result.group())
            else:
                img = qrcode.make(result.group())
            buf = BytesIO()
            img.save(buf)
            img_stream = buf.getvalue()
            result_img = base64.b64encode(img_stream)
            return JsonResponse({"msg": "success", "image": bytes.decode(result_img, 'utf-8')})
        else:
            return JsonResponse({"msg": "fail"})


class PicQRCodeView(View):
    def get(self, request):
        return render(request, 'makeCode_pics.html', {})


# 图片二维码
class MakePicCode(View):
    def post(self, request):
        src = request.body.decode('utf-8')
        # 检测用户上传文件是否为图片
        if src[9:14] != 'image':
            return JsonResponse({"msg": "fail"})
        # 定位文件所包含base64编码信息的位置并进行解码转换存入内存文件
        res = src.find('base64,')
        result_src = src[res + len('base64,'):]
        f = BytesIO()
        data = base64.b64decode(result_src)
        f.write(data)
        img = InMemoryUploadedFile(f, None, "image", len(data), None, None)
        # 将文件上传至云服务器
        leancloud.init('tiM1T9UGqwf6QTyXkn9kcL9z-gzGzoHsz', '1GzzyA6uv4l8JNGd6etu5V5o')
        execute = leancloud.File('image', img)
        execute.save()
        result_qrcode = qrcode.make(execute.url)
        buf = BytesIO()
        result_qrcode.save(buf)
        img_stream = buf.getvalue()
        result_img = base64.b64encode(img_stream)
        return JsonResponse({"msg": "success", "image": bytes.decode(result_img, 'utf-8')})


class FileCodeView(View):
    def get(self, request):
        return render(request, 'makeCode_files.html', {})


# 文件二维码
class MakeFileCode(View):
    def post(self, request):
        file_obj = request.FILES.get('file')
        if file_obj:
            print(file_obj)
            leancloud.init('tiM1T9UGqwf6QTyXkn9kcL9z-gzGzoHsz', '1GzzyA6uv4l8JNGd6etu5V5o')
            execute = leancloud.File('File', file_obj)
            execute.save()
            result_qrcode = qrcode.make(execute.url)
            buf = BytesIO()
            result_qrcode.save(buf)
            image_stream = buf.getvalue()
            resule_image = base64.b64encode(image_stream)
            return JsonResponse({"msg": "success", "image": bytes.decode(resule_image, 'utf-8')})
        return JsonResponse({"msg": 'fail'})
