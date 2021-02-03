from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import ImageLoader
from .forms import ImageLoaderForm, SizeChangeForm
from django.urls import reverse
from django.contrib import messages
from PIL import Image
from io import BytesIO
import requests
from django.core.files.base import ContentFile

def home(request):
    images = ImageLoader.objects.all()
    context = {'images' : images}
    return render(request, 'image_load_service/base.html', context)

def get_image(request, image_id : int, width : int, height : int):
    image = ImageLoader.objects.get(pk=image_id)
    img = Image.open(image.original_image.path)
    extention = image.original_image.path.split('.')[-1]
    output = BytesIO()
    if extention == 'jpg':
        extention = 'jpeg'
    size = (width, height)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(output, f"{extention.upper()}")
    return HttpResponse(output.getvalue(), content_type=f"image/{extention}")

def change_image(request, image_id):
    if request.method == "POST":
        image = ImageLoader.objects.get(pk=image_id)
        ch_form = SizeChangeForm(request.POST)
        if not ch_form.data['height'] and not ch_form.data['width']:
            messages.error(request,'Введите либо ширину, либо высоту, либо оба значения')
            width = image.original_image.width
            height = image.original_image.height
        elif ch_form.data['height'] and not ch_form.data['width']:
            height = ch_form.data['height']
            width = 100
        elif not ch_form.data['height'] and ch_form.data['width']:
            width = ch_form.data['width']
            height = 100
        else:
            width = ch_form.data['width']
            height = ch_form.data['height']
        change_form = SizeChangeForm()
        context = {'image': image, 'form': change_form, 'width': width,'height' : height, 'is_resize': 1 }
    else:
        image = ImageLoader.objects.get(pk=image_id)
        change_form = SizeChangeForm()
        context = {'image': image, 'form': change_form}
    return render(request, 'image_load_service/change_img_size.html', context)

def select_image(request):
    if request.method == "POST":
        ff = ImageLoaderForm(request.POST,request.FILES)
        if not ff.data['image_url'] and not ff.files.get('image_path') or ff.data['image_url'] and ff.files.get('image_path'):
            messages.error(request, 'Ошибка : Должно быть заполнено только одно поле')
            ff = ImageLoaderForm()
            context = {'form': ff}
            return render(request, 'image_load_service/create.html', context)
        elif ff.data['image_url'] and not ff.files.get('image_path'):
            response = requests.get(ff.data['image_url'])
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                thumb_io = BytesIO()
                filename = ff.data['image_url'].split('/')[-1]
                ext = filename.split('.')[-1]
                if ext == 'jpg':
                    ext = 'jpeg'
                elif ext == filename:
                    ext ='png'
                    filename = filename + f'.{ext}'
                img.save(thumb_io, format=ext.upper())
                file = ContentFile(thumb_io.getvalue())
                image = ImageLoader(title=filename)
                image.original_image.save(name = filename, content = file)
                image.save()
                change_form = SizeChangeForm()
                context = {'image': image, 'form': change_form}
                return HttpResponseRedirect(reverse(change_image, args=[image.pk]), request, context)
            else:
                ff = ImageLoaderForm()
                context = {'form': ff}
                return render(request, 'image_load_service/create.html', context)
        elif not ff.data['image_url'] and ff.files.get('image_path'):
            file = request.FILES['image_path']
            image = ImageLoader.objects.create(original_image = file, title = file.name)
            change_form = SizeChangeForm()
            context = {'image': image, 'form' : change_form}
            return HttpResponseRedirect(reverse(change_image, args=[image.pk]), request, context)
    else:
        ff = ImageLoaderForm()
        context = {'form' : ff}
        return render(request, 'image_load_service/create.html', context)

