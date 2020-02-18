from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 200)
    email = models.EmailField(max_length = 200)
    number_of_transactions = models.IntegerField(default = 0)
    number_of_positive_transactions = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

class Textbook(models.Model):
    class_object = models.ForeignKey(Class, on_delete = models.CASCADE)
    isbn = models.CharField(max_length = 13)
    #An ISBN Check is going to be needed here
    author = models.CharField(max_length = 200)
    title = models.CharField(max_length = 250)
    edition = models.CharField(max_length = 200)
    cover_photo = models.ImageField(upload_to = 'textbook_images')
    class_key = models.CharFiled(max_length = 200)
    
    def __str__(self):
        return self.title + " " + self.edition

    

