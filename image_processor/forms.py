from django import forms
from .models import UploadedImage


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']


class ImageProcessForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image', 'processed_image']
