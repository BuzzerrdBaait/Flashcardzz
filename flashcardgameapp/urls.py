from django.urls import path

from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views

from django.urls import path

from .views import home, create_deck, view_deck, create_card





app_name = "flashcardgameapp"

urlpatterns = [
     
    path('', views.home, name='home'),

    path('create_deck/', views.create_deck, name='create_deck'),

    path('view_deck/<int:deck_id>/', views.view_deck, name='view_deck'),

    path('create_card/<int:deck_id>/', views.create_card, name='create_card'),

    path('profile/<int:pk>/', views.user_profile_view, name="user_profile"),

    path('login/', views.login_user, name='login'),

    path('admin/', admin.site.urls),

    path('register/', views.register, name='register'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

