from django import forms

from .models import User_Profile, Deck, Card



   

class Registration(forms.Form):

    username = forms.CharField(label='Username', max_length=100)

    email = forms.EmailField(label='Email')

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)






class DeckForm(forms.ModelForm):

    class Meta:

        model = Deck

        fields = ['title', 'cover_photo_text']



class CardForm(forms.ModelForm):

    class Meta:

        model = Card

        fields = ['keywords', 'page_text']



class UserProfileForm(forms.ModelForm):

    class Meta:

        model = User_Profile

        fields = ['username', 'email']  # Add other fields as needed
