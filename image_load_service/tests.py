from django.test import TestCase
from django.urls import reverse
from .models import ImageLoader
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
import os
from test_project import settings

class ImageTests(TestCase):
    def setUp(self):
        full_path = os.path.join(settings.BASE_DIR, 'image_load_service') + '\\image_for_test.jpg'
        self.image=ImageLoader.objects.create(title='image_for_test.jpg')

    def test_image(self):
        self.assertEqual(f'{self.image.title}','image_for_test.jpg')

    def test_home_page(self):
        response=self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'Список изображений')
        self.assertTemplateUsed(response,'image_load_service/base.html')

# Create your tests here.
