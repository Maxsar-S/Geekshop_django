from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta

class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_created = models.DateTimeField(auto_now_add=True, blank = True, null=True)

    def is_activation_key_expired(self):
        if now() < self.activation_key_created + timedelta(hours=48):
            return True
        return False

class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOISES = (
        (MALE, 'M'),
        (FEMALE, 'W'),
    )

    user = models.OneToOneField(User, unique= True, null = False, db_index= True, on_delete= models.CASCADE)
    tagline = models.CharField(verbose_name='tags', max_length=128, blank= True)
    about_me = models.TextField(verbose_name='about me', max_length=128, blank=True)
    gender = models.CharField(choices=GENDER_CHOISES, blank= True, max_length=1, verbose_name='gender')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()