from django.urls import path


from authapp.views import login, register, logout, verify, ProfileUpdateView

app_name = 'authapp'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('profile/<int:pk>', ProfileUpdateView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),

    path('verify/<email>/<key>/', verify, name='verify')
]
