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
    template_name = 'index.html'

    def form_valid(self, form):
        uploaded_image = form.save()
        filter_effect = self.request.POST.get('filter_effect')

        # Validation to ensure filter_effect is a valid choice
        filter_effects = {
            'gaussian': ImageFilter.GaussianBlur(2),
            'box': ImageFilter.BoxBlur(2),
            'unsharp': ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3),
            'median': ImageFilter.MedianFilter(size=3),
            'min': ImageFilter.MinFilter(size=3),
            'max': ImageFilter.MaxFilter(size=3),
        }

        filter_function = filter_effects.get(filter_effect)

        if filter_function:
            img = Image.open(uploaded_image.image.path)
            processed_img = img.filter(filter_function)

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
            uploaded_image.filter_effect = filter_effect
            uploaded_image.save()

            return redirect('image_processor:display_image', pk=uploaded_image.pk)


class ImageDisplayView(TemplateView):
    template_name = 'display.html'
    form_class = ImageProcessForm

    def get(self, request, *args, **kwargs):
        image_id = self.kwargs['pk']
        uploaded_image = UploadedImage.objects.get(pk=image_id)
        form = self.form_class(instance=uploaded_image)
        context = {
            "form": form
        }
        return self.render_to_response(context)
