from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.user_login, name='login'),  # Root URL redirects to login page
    path('colorizer_home/', views.colorizer_home, name='colorizer_home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),  # Updated to user_login
    # Add other URLs as needed for your project

     path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('images/', views.image_list, name='image_list'),
    path('images/add/', views.image_add, name='image_add'),
    path('images/edit/<int:id>/', views.image_edit, name='image_edit'),
    path('images/delete/<int:id>/', views.image_delete, name='image_delete'),
    path('admin-login/', views.admin_login, name='admin_login'),

    path('home', views.home, name='home'),
    
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)