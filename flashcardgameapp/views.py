from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.views import View 
from .models import User_Profile,Deck, Card
from django.http import HttpResponse
from .forms import Registration
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import DeckForm, CardForm, DeleteCardForm, DeleteDeckForm
from collections import OrderedDict
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()



def home(request):

    """_____I imported OrderedDict and created an instance of a dictionary of the Deck.Category choices
    _____It sorts by the id # so I had to call lambda function and key[1] is used because the keywords 
    _____are in that column. So basically this is how to sort your items by the category choices defined
    _____in the model's category dictionary.

    """

    user_decks = Deck.objects.all()

    public_decks_by_category = {}

    category_choices_dict = dict(Deck.CATEGORY_CHOICES)

    sorted_categories = OrderedDict(sorted(category_choices_dict.items(), key=lambda key: key[1]))

    for category in sorted_categories.keys():

        public_decks_by_category[category] = Deck.objects.filter(public=True, category=category).order_by('category')


    return render(request, 'home.html', {

        'user_decks': user_decks,

        'public_decks_by_category': public_decks_by_category,

    })


def user_profile_view(request, user_pk):

    user = get_object_or_404(User, pk=user_pk)

    user_decks = Deck.objects.filter(user=user)



    if request.method == 'POST':

        for deck in user_decks:

            public_checkbox_name = f'public_{deck.id}'

            if public_checkbox_name in request.POST:

                deck.public = True

            else:

                deck.public = False

            deck.save()

    




    return render(request, 'user_profile.html', {'user_decks': user_decks})



def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(request, username=username, password=password)



        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            error_message = "Invalid credentials"

            return render(request, 'Error.html', {'error_message': error_message})

    else:

        return render(request, 'login.html')


def register(request):

    """
    This creates a user model based on the User_Profile model which is the base User model extended.
    """

    if request.method == 'POST':

        form = Registration(request.POST)

        if form.is_valid():


            user_data = form.cleaned_data

            new_user = User_Profile.objects.create_user(

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
            

            return redirect('login')

    else:

        form = Registration()

    return render(request, 'Registration.html', {'form': form})


@login_required


@login_required

def create_deck(request):

    """
    Imported this Deck Form so users can have a view to create new decks
    """

    if request.method == 'POST':

        form = DeckForm(request.POST)

        if form.is_valid():

            deck = form.save(commit=False)

            deck.user = request.user

            deck.save()

            return redirect('home')

    else:

        form = DeckForm()

    return render(request, 'create_deck.html', {'form': form})





def view_deck(request, deck_id):

    deck = get_object_or_404(Deck, id=deck_id)


    cards = Card.objects.filter(deck=deck)

    delete_deck_form = DeleteDeckForm()  # Initialize delete_deck_form here



    if request.method == 'POST':

        delete_card_form = DeleteCardForm(request.POST)

        delete_deck_form = DeleteDeckForm(request.POST)



        if delete_card_form.is_valid():

            card_id = delete_card_form.cleaned_data['card_id']

            card_to_delete = get_object_or_404(Card, id=card_id, deck=deck)

            card_to_delete.delete()


        return redirect('view_deck', deck_id=deck.id)

    else:

        delete_card_form = DeleteCardForm()



    return render(request, 'view_deck.html', {'deck': deck, 'cards': cards, 'delete_card_form': delete_card_form})

@login_required

def create_card(request, deck_id):

    # Create a new flashcard within a deck

    deck = Deck.objects.get(id=deck_id)

    if request.method == 'POST':

        form = CardForm(request.POST)

        if form.is_valid():

            card = form.save(commit=False)

            card.deck = deck

            card.save()

            return redirect('view_deck', deck_id=deck.id)

    else:

        form = CardForm()

    return render(request, 'create_card.html', {'form': form, 'deck': deck})




def edit_deck(request, deck_id):

    deck = get_object_or_404(Deck, id=deck_id)



    if request.method == 'POST':

        form = DeckForm(request.POST, instance=deck)

        if form.is_valid():

            deck_instance = form.save(commit=False)

            # Get the value of the checkbox and set it to True/False

            deck_instance.public = request.POST.get('public', False) == 'on'

            deck_instance.save()

            return redirect('view_deck', deck_id=deck_id)

    else:

        form = DeckForm(instance=deck)



    return render(request, 'edit_deck.html', {'form': form, 'deck': deck})

