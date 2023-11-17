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


class Deck(models.Model):

    user = models.ForeignKey(User_Profile, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()  # Text field instead of ImageField

    public= models.BooleanField(default=False)

    CATEGORY_CHOICES=[

        ('Science','Science'),
        ('Technology','Technology'),
        ('Engineering','Engineering'),
        ('Mathematics','Mathematics'),
        ('History','History'),
        ('Literature','Literature'),
        ('Languages','Languages'),
        ('Arts','Arts'),
        ('Health and Medicine','Health & Medicine'),
        ('Programming','Programming'),
        ('Misc','Misc.'),
        
    ]

    category= models.CharField(max_length=25, default='Misc', choices=CATEGORY_CHOICES)



    def __str__(self):

        return self.title



class Card(models.Model):

    # Represents a flashcard

    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)

    question = models.CharField(max_length=5000, blank=True)

    answer = models.TextField()  # Text field instead of ImageField



    def __str__(self):

        return f"Card {self.pk} of {self.deck.title}"



