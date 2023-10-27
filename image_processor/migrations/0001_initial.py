# Generated by Django 4.2.6 on 2023-10-27 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('processed_image', models.ImageField(blank=True, null=True, upload_to='processed/')),
                ('filter_effect', models.CharField(choices=[('gaussian', 'Gaussian Blur'), ('box', 'Box Blur'), ('unsharp', 'Unsharp Mask'), ('median', 'Median Filter'), ('min', 'Min Filter'), ('max', 'Max Filter')], default='gaussian', max_length=50)),
            ],
        ),
    ]
