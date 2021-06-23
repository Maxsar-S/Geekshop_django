from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from authapp.models import User
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'title': 'GeekShop - Авторизация', 'form': form}
    return render(request, 'authapp/login.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            send_verify_link(user)
            messages.success(request, 'Вы успешно зарегестрировались! \n Ссылка для активация аккаунта отправлена на почту')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {'title': 'GeekShop - Регистрация', 'form': form}
    return render(request, 'authapp/register.html', context)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'authapp/profile.html'
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse('users:profile', args=[self.object.pk])

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop Admin - Личный кабинет'
        context['baskets'] = Basket.objects.filter(user=self.object.pk)
        return context


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def send_verify_link(user):
    verify_link= reverse('users:verify', args=[user.email, user.activation_key])
    subject = 'Account verify'
    message = f'Your link for account activation: {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

def verify(request, email, key):
    user = User.objects.filter(email=email).first()

    if user and user.activation_key == key and not user.is_activation_key_expired():
        user.is_active = True
        user.activation_key = ''
        user.activation_key_created = None
        user.save()
        auth.login(request, user)
    return render(request, 'authapp/verify.html')