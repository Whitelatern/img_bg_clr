from django.db import models

from django.contrib.auth.models import User



class ImageUpload(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # Allow blank and null values
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
    
