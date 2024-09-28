from django.db import models

from django.contrib.auth.models import User



class ImageUpload(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # Allow blank and null values
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
    
class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_input = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
