from django.urls import path
from . views import home, select_image, change_image, get_image

urlpatterns = [
    path('get_image/<int:image_id>/<int:width>/<int:height>/', get_image, name='get_image'),
    path('change/<int:image_id>/', change_image, name='change'),
    path('add/', select_image, name='add'),
    path('', home, name='home'),
]