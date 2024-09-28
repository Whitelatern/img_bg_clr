from django import forms
from .models import ImageUpload

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['name', 'description', 'image']


from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()



