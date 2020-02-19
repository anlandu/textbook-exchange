from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.
"""class User(models.Model):
    name = models.CharField(max_length = 200)
    email = models.EmailField(max_length = 200)
    number_of_transactions = models.IntegerField(default = 0)
    number_of_positive_transactions = models.IntegerField(default = 0)

    def __str__(self):
        return self.name
"""
#Going to use the custom user model provided by Django

class Textbook(models.Model):
    class_object = models.ForeignKey(User, on_delete = models.CASCADE)
    isbn = models.CharField(max_length = 13)
    #An ISBN Check is going to be needed here
    author = models.CharField(max_length = 200)
    title = models.CharField(max_length = 250)
    edition = models.CharField(max_length = 200)
    cover_photo = models.ImageField(upload_to = 'textbook_images')
    class_key = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.title + " " + self.edition

class Class(models.Model):
    department = models.CharField(max_length = 200)
    subject = models.CharField(max_length = 200)
    title = models.CharField(max_length = 200)
    class_code = models.IntegerField(default = 0)
    section_number = models.CharField(max_length = 10)
    professor = models.CharField(max_length = 200)

    def __str__(self):
        return self.subject + self.class_code

class Listing(models.Model):
    #foreign key to user
    textbook = models.ForeignKey(Textbook, on_delete = models.CASCADE)
    class_object = models.ForeignKey(Class, on_delete = models.CASCADE)
    condition = models.IntegerField(default = 0)
    picture = models.ImageField(upload_to = 'listing_images')
    comments = models.ArrayField(models.CharField(max_length = 500), blank = True)
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    hasBeenSoldFlag = models.BooleanField()

    def __str__(self):
        return self.textbook

    

