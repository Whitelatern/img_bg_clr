from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import ImageUploadForm
from colorizers import eccv16, preprocess_img, postprocess_tens
import torch
import os
from django.conf import settings
from PIL import Image
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect, get_object_or_404
from .models import ImageUpload
from .forms import ImageUploadForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages  # Import messages module
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.shortcuts import render
from .models import ImageUpload


def colorizer_home(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES['image']
            
            # Ensure 'imgs' directory exists
            img_dir = os.path.join(settings.MEDIA_ROOT, 'imgs')
            os.makedirs(img_dir, exist_ok=True)
            
            # Save the uploaded file
            image_path = os.path.join(img_dir, img.name)
            with open(image_path, 'wb+') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)
            
            try:
                # Load image as numpy array
                img = Image.open(image_path)
                img_rgb_orig = np.asarray(img)
                
                # Convert to RGB if image is not already in RGB format
                if img_rgb_orig.ndim != 3 or img_rgb_orig.shape[2] != 3:
                    img = img.convert('RGB')
                    img_rgb_orig = np.asarray(img)
                
                tens_l_orig, tens_l_rs = preprocess_img(img_rgb_orig, HW=(256, 256))
                
                # Perform colorization
                colorizer_eccv16 = eccv16(pretrained=True).eval()
                
                if torch.cuda.is_available():
                    colorizer_eccv16.cuda()
                    tens_l_rs = tens_l_rs.cuda()
                
                out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
                
                # Convert the output to base64 to render in the template
                plt.imsave(BytesIO(), out_img_eccv16)
                buffer = BytesIO()
                plt.imsave(buffer, out_img_eccv16, format='png')
                out_img_eccv16_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                # Pass the processed data to the template for rendering
                return render(request, 'colorizer_result.html', {'image_path': img, 'out_img_eccv16': out_img_eccv16_base64})
            
            except Exception as e:
                error_message = str(e)
                return render(request, 'error.html', {'error_message': error_message})
    
    else:
        form = ImageUploadForm()
    
    return render(request, 'colorizer_home.html', {'form': form})

# def colorizer_home(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             img = request.FILES['image']
            
#             # Ensure 'imgs' directory exists
#             img_dir = os.path.join(settings.MEDIA_ROOT, 'imgs')
#             os.makedirs(img_dir, exist_ok=True)
            
#             # Save the uploaded file
#             image_path = os.path.join(img_dir, img.name)
#             with open(image_path, 'wb+') as destination:
#                 for chunk in img.chunks():
#                     destination.write(chunk)
            
#             try:
#                 # Load image as numpy array
#                 img = Image.open(image_path)
#                 img_rgb_orig = np.asarray(img)
                
#                 # Convert to RGB if image is not already in RGB format
#                 if img_rgb_orig.ndim != 3 or img_rgb_orig.shape[2] != 3:
#                     img = img.convert('RGB')
#                     img_rgb_orig = np.asarray(img)
                
#                 tens_l_orig, tens_l_rs = preprocess_img(img_rgb_orig, HW=(256, 256))
                
#                 # Perform colorization
#                 colorizer_eccv16 = eccv16(pretrained=True).eval()
                
#                 if torch.cuda.is_available():
#                     colorizer_eccv16.cuda()
#                     tens_l_rs = tens_l_rs.cuda()
                
#                 out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
                
#                 # Convert the output to base64 to render in the template
#                 buffer = BytesIO()
#                 plt.imsave(buffer, out_img_eccv16, format='png')
#                 out_img_eccv16_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
#                 # Pass the processed data to the template for rendering
#                 return render(request, 'colorizer_result.html', {'image_path': img, 'out_img_eccv16': out_img_eccv16_base64})
            
#             except Exception as e:
#                 error_message = str(e)
#                 return render(request, 'error.html', {'error_message': error_message})
    
#     else:
#         form = ImageUploadForm()
    
#     return render(request, 'colorizer_home.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # use password1 for UserCreationForm
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')  # Redirect to login page after successful registration
        else:
            # Handling different error scenarios
            if 'password1' in form.errors and 'password2' in form.errors:
                message = "Passwords do not match."
            else:
                message = "Invalid form submission. Please correct the errors."

            # Using Django's messages framework to pass messages to the template
            messages.error(request, message)
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # Redirect to colorizer_home page after successful login
            else:
                messages.error(request, 'Invalid username or password. Please try again.')  # Add error message
        else:
            messages.error(request, 'Invalid username or password. Please try again.')  # Add error message
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:  # Ensure only superusers can log in here
                    auth_login(request, user)
                    return redirect('admin_dashboard')  # Redirect to admin dashboard
                else:
                    messages.error(request, 'You are not authorized to access this page.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'admin_login.html', {'form': form})


# Admin dashboard
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Image list
def image_list(request):
    images = ImageUpload.objects.all()
    return render(request, 'image_list.html', {'images': images})

# # Add image
# def image_add(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('image_list')
#     else:
#         form = ImageUploadForm()
#     return render(request, 'image_add.html', {'form': form})
# Add image view
def image_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        image = request.FILES.get('image')

        if name and image:
            print(f"Uploading: {image.name}")  # For debugging
            new_image = ImageUpload(name=name, description=description, image=image)
            new_image.save()
            return redirect('image_list')

    return render(request, 'image_add.html')



from django.shortcuts import render, get_object_or_404, redirect
from .models import ImageUpload

def image_edit(request, id):
    image = get_object_or_404(ImageUpload, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        new_image = request.FILES.get('image')

        # Update image fields
        image.name = name
        image.description = description

        if new_image:  # Only update image if a new one is uploaded
            image.image = new_image

        image.save()  # Save the updated image object

        return redirect('image_list')

    return render(request, 'image_edit.html', {'image': image})


# Delete image
def image_delete(request, id):
    image = get_object_or_404(ImageUpload, id=id)
    if request.method == 'POST':
        image.delete()
        return redirect('image_list')
    return render(request, 'image_delete.html', {'image': image})


# views.py

def home(request):
    # Query all images from the database
    images = ImageUpload.objects.all()
    return render(request, 'home.html', {'images': images})

from django.shortcuts import render
from .models import ImageUpload

def home_view(request):
    images = ImageUpload.objects.all()  # Fetch all the images from the database
    return render(request, 'home.html', {'images': images})
