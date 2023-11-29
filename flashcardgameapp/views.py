from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.views import View 
from .models import User_Profile,Deck, Card,WebImgs, Contact
from django.http import HttpResponse
from .forms import Registration
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import DeckForm, CardForm, DeleteCardForm, DeleteDeckForm
from collections import OrderedDict
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .forms import ContactForm

from django.urls import reverse


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

    




    return render(request, 'user_profile.html', {'user_decks': user_decks, 'user':user})



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

                registration_link = request.build_absolute_uri(

                    reverse('authenticate_user', args=[str(new_user.authentication_link)])

                )

                send_mail(

                    f"Welcome {new_user.username}",

                    f"Welcome to Flashcardzz!\n\n Here is how to get registered:\n\nBelow is your authentication key.\n\ncopy this:\n\n{new_user.authentication_key} \n\nClick the link below to complete your registration:\n\n{registration_link}",

                    "admin@ilovecookbooks.org",

                    [new_user.email],

                    fail_silently=False,

                )

            except:

                print("Sending an email failed")

            return redirect('login')

    else:

        form = Registration()

    return render(request, 'Registration.html', {'form': form})



@login_required

def create_deck(request):

    """
    Imported this Deck Form so users can have a view to create new decks
    """

    if request.method == 'POST':
        

            user = request.user

            user_decks_count = Deck.objects.filter(user=user).count()


            if user.is_verified == 'N' and user_decks_count >= 5:

                print('MAX LIMIT REACHED FOR UNAUTH USER')

                return redirect('home')


            if user.is_verified == 'Y' and user_decks_count >= 20:

                print("MAX LIMIT REACHED FOR AUTH USER")

                return redirect('user_profile', user_pk=request.user.pk)



            form = DeckForm(request.POST)

            if form.is_valid():

                deck = form.save(commit=False)

                deck.user = request.user

                deck.save()

            return redirect('user_profile', user_pk=request.user.pk)

    else:

        form = DeckForm()

    return render(request, 'create_deck.html', {'form': form})





def view_deck(request, deck_id):

    deck = get_object_or_404(Deck, id=deck_id)

    images=WebImgs.objects.all()

    flip_button=images[1]

    left=images[0]

    right=images[2]

    flashcard=images[3]

    back=images[4]

    cards = Card.objects.filter(deck=deck)

    delete_deck_form = DeleteDeckForm() 



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



    return render(request, 'view_deck.html', {'deck': deck, 'cards': cards, 'delete_card_form': delete_card_form, 'flip_button':flip_button, 'left':left,'right': right,'flashcard':flashcard, 'back':back})

@login_required

def create_card(request, deck_id):

    # Create a new flashcard within a 
    
    print("BEFORE DECK TRIGGERED")

    deck = Deck.objects.get(id=deck_id)

    if request.method == 'POST':

        user = request.user


        user_card_count = Card.objects.filter(deck__user=user).count()


        if user.is_verified == 'N' and user_card_count >= 250:

                return redirect('home')



        if user.is_verified == 'Y' and user_card_count >= 2000:


                return redirect('user_profile', user_pk=request.user.pk)
        

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

            delete_form = DeleteDeckForm(request.POST)



            if delete_form.is_valid():

                deck.delete()

                return redirect('user_profile', user_pk=request.user.pk)



            if form.is_valid():

                deck_instance = form.save(commit=False)

                deck_instance.public = request.POST.get('public', False) == 'on'

                deck_instance.save()

                return redirect('view_deck', deck_id=deck_id)

    else:

            form = DeckForm(instance=deck)

            delete_form = DeleteDeckForm(initial={'deck_id': deck_id})



    return render(request, 'edit_deck.html', {'form': form, 'delete_deck_form': delete_form, 'deck': deck})


def about_us(request):

    print("about us triggered")

    return render(request, 'about_us.html')


def clep_resources(request):

    print("clep_resources")

    return render(request, 'clep_resources.html')




def contact_view(request):

    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():

            contact_data = form.cleaned_data


            Contact.objects.create(**contact_data)

            try:

                send_mail(

                    f"Hello {contact_data['name']}!",

                    "We have received your message and will get back to you as soon as possible.",

                    "admin@ilovecookbooks.com",

                    [contact_data['email']],

                    fail_silently=False,

                )

            except Exception as e:

                print(f"Sending email failed: {e}")



            # Redirect to a thank you page or wherever you want

            return redirect('home')

    else:

        form = ContactForm()



    return render(request, 'contact_us.html', {'form': form})




from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from .models import User_Profile

from .forms import AuthenticationForm



def authenticate_user(request, authentication_link):

    user_profile = get_object_or_404(User_Profile, authentication_link=authentication_link)



    if request.method == 'POST':

        form = AuthenticationForm(request.POST)

        if form.is_valid():

            authentication_key = form.cleaned_data['authentication_key']



            # Check if the provided authentication key matches the one in the user profile

            if authentication_key == user_profile.authentication_key:

                # Update the is_verified field

                user_profile.is_verified = 'Y'

                user_profile.save()

                return render(request, 'auth_success.html', {'user_profile': user_profile})



    else:

        form = AuthenticationForm()



    return render(request, 'auth.html', {'form': form, 'user_profile': user_profile})





