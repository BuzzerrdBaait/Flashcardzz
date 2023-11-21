from django.urls import path

from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views

from django.urls import path

from .views import home, create_deck, view_deck, create_card, about_us, contact_us, clep_resources





app_name = "flashcardgameapp"

urlpatterns = [
     
    path('', views.home, name='home'),

    path('create_deck/', views.create_deck, name='create_deck'),

    path('view_deck/<int:deck_id>/', views.view_deck, name='view_deck'),

    path('deck/<int:deck_id>/edit/', views.edit_deck, name='edit_deck'),

    path('create_card/<int:deck_id>/', views.create_card, name='create_card'),

    path('profile/<int:user_pk>/', views.user_profile_view, name='user_profile'),

    path('about', views.about_us, name='about_us'),

    path('contact', views.contact_us, name='contact'),

    path('clep', views.clep_resources, name='clep'),

    path('login/', views.login_user, name='login'),

    path('logout', auth_views.LogoutView.as_view(), name='logout'),

    path('admin/', admin.site.urls),

    path('register/', views.register, name='register'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]

