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

        # Process the uploaded image using Pillow (GaussianBlur, for example)
        img = Image.open(uploaded_image.image.path)
        processed_img = img.filter(ImageFilter.GaussianBlur(2))  # Apply GaussianBlur

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
