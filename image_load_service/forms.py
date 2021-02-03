from django import forms

class ImageLoaderForm(forms.Form):
    image_url = forms.URLField(label="Ссылка",required=False)
    image_path = forms.FileField(label="Файл", required=False)

class SizeChangeForm(forms.Form):
    width = forms.CharField(label="Ширина",required=False)
    height = forms.CharField(label="Высота",required=False)
