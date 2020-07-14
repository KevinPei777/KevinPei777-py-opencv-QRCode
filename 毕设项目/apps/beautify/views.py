from django.shortcuts import render
from django.views.generic.base import View
from django.http.response import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO
import os
from MyQR import myqr
# Create your views here.


class CodeBeautify(View):
    def get(self, request):
        return render(request, 'Code_beautify.html', {})


class MakeNewCode(View):
    def post(self, request):
        file_obj = request.FILES.get('file')
        text = request.POST['src']
        image_format = ['.jpg', '.png', '.bmp', '.gif']
        format_2 = file_obj.name[-4:]
        if text[5:10] != 'image' or format_2 not in image_format:
            return JsonResponse({"msg": "Not_Img"})
        index = text.find('base64,')
        cache_data = text[index + len('base64,'):]
        data = base64.b64decode(cache_data)
        f = BytesIO()
        f.write(data)
        cache_img = Image.open(f)
        qr_data = decode(cache_img)
        if not qr_data:
            return JsonResponse({"msg": "No_QRCode"})
        qr_text = qr_data[0].data.decode('utf8')
        path = os.getcwd() + '\static\img\\'
        try:
            if format_2 == '.gif':
                if os.path.exists(path + 'back.gif'):
                    os.remove(path + 'back.gif')
                save_back_gif = default_storage.save(path + 'back.gif', ContentFile(file_obj.read()))
                myqr.run(qr_text, picture=path + 'back.gif', colorized=True,
                         save_name='final.gif', save_dir=os.getcwd() + '\static\img')
                with open(path + 'final.gif', 'rb') as file:
                    byte = file.read()
                image_base64 = base64.b64encode(byte)
                return JsonResponse({"msg": 'gif', "code": bytes.decode(image_base64, 'utf8')})
            else:
                if os.path.exists(path + 'back.png'):
                    os.remove(path + 'back.png')
                save_back_png = default_storage.save(path + 'back.png',
                                                     ContentFile(file_obj.read()))
                myqr.run(qr_text, picture=path + 'back.png', colorized=True,
                         save_name='final.png', save_dir=os.getcwd() + '\static\img')
                with open(path + 'final.png', 'rb') as file:
                    byte = file.read()
                image_base64 = base64.b64encode(byte)
                return JsonResponse({"msg": 'png', "code": bytes.decode(image_base64, 'utf8')})
        except ValueError:
            return JsonResponse({"msg": "chinese"})
