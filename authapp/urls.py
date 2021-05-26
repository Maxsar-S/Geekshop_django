from django.urls import path

from authapp.views import login, RegisterCreateView, logout, ProfileUpdateView

app_name = 'authapp'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('profile/<int:pk>', ProfileUpdateView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
]
