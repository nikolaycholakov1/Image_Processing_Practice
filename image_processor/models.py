from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_image = models.ImageField(upload_to='processed/', blank=True, null=True)
    filter_effect = models.CharField(max_length=50, choices=[
        ('gaussian', 'Gaussian Blur'),
        ('box', 'Box Blur'),
        ('unsharp', 'Unsharp Mask'),
        ('median', 'Median Filter'),
        ('min', 'Min Filter'),
        ('max', 'Max Filter')
    ], default='gaussian')

