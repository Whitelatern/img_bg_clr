from django.contrib import admin
from .models import ImageUpload

class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')  # Adjust the fields based on your model

admin.site.register(ImageUpload, ImageUploadAdmin)
