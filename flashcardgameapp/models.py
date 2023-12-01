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



    """
    AUTHENTICATION LINK CODE
    """
    authentication_link = models.CharField(max_length=50, default='authenticate_your_acct')

    def generate_unique_link(self):

        link = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(30))

        link = link.replace('\\', str(secrets.randbelow(1000)))

        link = link.replace('/', str(secrets.randbelow(1000)))

        link = link.replace("'", str(secrets.randbelow(1000)))

        link = link.replace('"', str(secrets.randbelow(1000)))

        return link



    def save(self, *args, **kwargs):

        if not self.authentication_key:

            self.authentication_key = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(30))


        if not self.authentication_link:

            self.authentication_link = self.generate_unique_link()


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


    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)

    question = models.TextField()

    answer = models.TextField() 


    def __str__(self):

        return f"Card {self.pk} of {self.deck.title}"
    

class WebImgs(models.Model):

    title= models.CharField(max_length=32,blank=True)

    image= models.ImageField(upload_to='web_imgs/')

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)



class Contact(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    message = models.TextField()

    current_date = models.DateTimeField(auto_now_add=True)


