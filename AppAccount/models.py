from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    SEXE=(('M','M'),
          ('F','F'))
    username=models.CharField(max_length=254)
    last_name=models.CharField(max_length=254)
    email=models.EmailField(max_length=254, unique=True)
    genre=models.CharField(max_length=1, choices=SEXE)
    biography=models.TextField(null=True, blank=True)
    image=models.ImageField(upload_to='profil',null=True, blank=True)
    confirme_password=models.CharField(max_length=254)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

    USERNAME_FIELD='email'

    REQUIRED_FIELDS=['username','last_name','genre']

    @property
    def getUser(self):
        return f'{self.username} {self.last_name}'

    
    


    def __str__(self):
        return self.username
