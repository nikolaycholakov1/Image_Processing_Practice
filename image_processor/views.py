from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .models import UploadedImage
from .forms import ImageUploadForm, ImageProcessForm
from PIL import Image, ImageFilter
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class ImageProcessView(FormView):
    form_class = ImageUploadForm
    template_name = 'main.html'

    def form_valid(self, form):
        uploaded_image = form.save()
        filter_effect = self.request.POST.get('filter_effect')  # Get the selected filter effect

        # Clear the processed_image field when a new image is processed
        if uploaded_image.processed_image:
            uploaded_image.processed_image.delete()

        # Process the uploaded image using the selected filter effect
        img = Image.open(uploaded_image.image.path)
        if filter_effect == 'gaussian':
            processed_img = img.filter(ImageFilter.GaussianBlur(2))
        elif filter_effect == 'box':
            processed_img = img.filter(ImageFilter.BoxBlur(2))
        elif filter_effect == 'unsharp':
            processed_img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        elif filter_effect == 'median':
            processed_img = img.filter(ImageFilter.MedianFilter(size=3))
        elif filter_effect == 'min':
            processed_img = img.filter(ImageFilter.MinFilter(size=3))
        elif filter_effect == 'max':
            processed_img = img.filter(ImageFilter.MaxFilter(size=3))

        # Save the processed image
        buffer = BytesIO()
        processed_img.save(buffer, format='JPEG')
        processed_image = InMemoryUploadedFile(
            buffer,
            None,
            'processed.jpg',
            'image/jpeg',
            buffer.tell(),
            None
        )
        uploaded_image.processed_image = processed_image
        uploaded_image.filter_effect = filter_effect  # Store the chosen filter effect
        uploaded_image.save()

        # Redirect to the display view with the pk of the processed image
        return redirect('image_processor:display_image', pk=uploaded_image.pk)


class ImageDisplayView(TemplateView):
    template_name = 'display.html'
    form_class = ImageProcessForm

    def get(self, request, *args, **kwargs):
        image_id = self.kwargs['pk']
        uploaded_image = UploadedImage.objects.get(pk=image_id)
        form = self.form_class(instance=uploaded_image)
        return self.render_to_response({'form': form})
