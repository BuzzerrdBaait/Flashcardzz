from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import DetailView 
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.views import View 
from .models import User_Profile

from django.http import HttpResponse

from .forms import Registration
from django.http import HttpResponseForbidden


def home(request):
     test="teeest"
     context = {

        'test': test,

    }

     return render(request, 'home.html', context)


def user_profile_view(request):
     user_name='test'

     context= {

          'username':user_name,
     }

     return render(request, 'User_Profile.html',context)




def login_user(request):
    print('login user tripped')



    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            print("user is not none")

            login(request, user)


            return redirect('flashcardgameapp:Home')

        else:

            # Display an error message

            error_message = "Invalid credentials"

            return render(request, 'Error.html', {'error_message': error_message})

    else:
        print("rendering home.html")

        return render(request, 'login.html')


def register(request):

    if request.method == 'POST':

        form = Registration(request.POST)

        if form.is_valid():

            # Create a new user account using Django's User model

            user_data = form.cleaned_data

            new_user = User.objects.create_user(

                username=user_data['username'],

                email=user_data['email'],

                password=user_data['password'],

            )

            try:

                send_mail(
                    f"Welcome {new_user.username}",
                    "Thank you for joining the cookbook movement! It is with great joy that I present ilovecookbooks.org. Heres what you have the power to do: First, I encourage you to navigate to your user profile and set a profile picture. There's plenty of ai generated photos to choose from, or you can upload your own. Second, create new books on your profile page. Then as you browse the cookbooks on this website you will be able to save pages that you like to whichever category you defined! That's the magic of it! Enjoy! ",
                    "admin@ilovecookbooks.org",
                    [new_user.email],
                    fail_silently=False,
                )

            except:

                print("sending an email failed")
            

            return redirect('flashcardgameapp:login')

    else:

        form = Registration()

    return render(request, 'Registration.html', {'form': form})