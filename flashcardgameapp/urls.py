from django.urls import path

from . import views



app_name = "flashcardgameapp"

urlpatterns = [

    path("", views.home, name="home"),

    path('profile/<int:pk>/', views.user_profile_view, name="user_profile"),

    path('login/', views.login_user, name='login'),

    path('register/', views.register, name='register'),

]

