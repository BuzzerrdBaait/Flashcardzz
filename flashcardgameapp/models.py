import secrets

import string

from django.contrib.auth.models import AbstractUser, Group, Permission

from django.db import models



class User_Profile(AbstractUser):
    
    email= models.CharField(max_length=40,blank=True,null=True, unique=True)

    authentication_key = models.CharField(max_length=50, unique=True)

    is_verified = models.CharField(max_length=1, default='N')

    user_image = models.ImageField(upload_to='user_images/', blank=True, null=True)

    user_library = models.CharField(max_length=255, default='', blank=True)



    def save(self, *args, **kwargs):

        # Generate authentication key before saving

        if not self.authentication_key:

            self.authentication_key = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(30))



        super().save(*args, **kwargs)

