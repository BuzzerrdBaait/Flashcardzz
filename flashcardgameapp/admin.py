from django.contrib import admin

from .models import User_Profile
# Register your models here.



class User_Profile_Admin(admin.ModelAdmin):

    list_display = ('username','email','date_joined','is_verified','user_image','id')

    search_fields = ('username', 'date_joined', 'is_verified')

    prepopulated_fields = {'username': ('username',)}




admin.site.register(User_Profile, User_Profile_Admin)

