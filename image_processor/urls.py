from django.urls import path
from .views import ImageProcessView, ImageDisplayView

app_name = 'image_processor'

urlpatterns = [
    path('', ImageProcessView.as_view(), name='upload_and_process'),
    path('display/<int:pk>/', ImageDisplayView.as_view(), name='display_image'),
]
