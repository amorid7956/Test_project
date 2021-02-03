from django.db import models

class ImageLoader(models.Model):
    title = models.CharField(max_length=40, verbose_name='Название')
    original_image = models.ImageField(verbose_name='Оригинальное изображение',
                                       upload_to='images/',blank= True, null=True)
    published = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Изображеие'
        verbose_name_plural = 'Изображеия'
        ordering = ['-published']

    def __str__(self):
        return self.title




# Create your models here.
