from django.contrib import admin

from .models import User_Profile,WebImgs,Contact



class User_Profile_Admin(admin.ModelAdmin):

    list_display = ('username','email','date_joined','is_verified','user_image','id')

    search_fields = ('username', 'date_joined', 'is_verified')

    prepopulated_fields = {'username': ('username',)}




admin.site.register(User_Profile, User_Profile_Admin)



class web_img_admin(admin.ModelAdmin):

    list_display=('title','image')

admin.site.register(WebImgs,web_img_admin)






class ContactAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'current_date')

    search_fields = ('name', 'email', 'message')

    list_filter = ('current_date',)

    ordering = ('-current_date',)

admin.site.register(Contact,ContactAdmin)
