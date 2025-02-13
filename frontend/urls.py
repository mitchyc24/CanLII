from django.urls import path
from. import views  # Import your views from the current directory

urlpatterns = [
    path('', views.home, name='home'),  # Map the root URL to the home view
]