from django import forms
from .models import UploadedImage


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']


class ImageProcessForm(forms.ModelForm):
    FILTER_CHOICES = [
        ('gaussian', 'Gaussian Blur'),
        ('box', 'Box Blur'),
        ('unsharp', 'Unsharp Mask'),
        ('median', 'Median Filter'),
        ('min', 'Min Filter'),
        ('max', 'Max Filter')
    ]

    filter_effect = forms.ChoiceField(choices=FILTER_CHOICES, required=True)

    class Meta:
        model = UploadedImage
        fields = ['image']
