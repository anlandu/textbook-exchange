from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models, Field
from django.utils import timezone


# Create your models here.
#Django User Model
class User(AbstractUser):
    # username = models.CharField(_('username'), max_length = 30, unique = True)
    # first_name = models.CharField(_('first name'), max_length = 30, blank = True)
    # last_name = models.CharField(_('last name'), max_length = 30, blank = True)
    # email = models.EmailField(_('email address'), blank = True)
    # password = models.CharField(_('password'), max_length = 30)
    # is_staff = models.BooleanField(_('staff status'), default = False)
    # date_joined = models.DateTimeField(_('date joined'), default = timezone.now)

    username = models.CharField(max_length = 30, unique = True)
    first_name = models.CharField(max_length = 30, blank = True)
    last_name = models.CharField(max_length = 30, blank = True)
    email = models.EmailField(, blank = True)
    password = models.CharField(max_length = 30)
    is_staff = models.BooleanField(default = False)
    date_joined = models.DateTimeField(default = timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

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
        textbook = '%s %s' % (self.title, self.edition)
        return textbook.strip()

class Class(models.Model):
    department = models.CharField(max_length = 200)
    subject = models.CharField(max_length = 200)
    title = models.CharField(max_length = 200)
    class_code = models.IntegerField(default = 0)
    section_number = models.CharField(max_length = 10)
    professor = models.CharField(max_length = 200)

    def __str__(self):
        class_info = '%s%s' % (self.subject, self.class_code)
        return class_info.strip()

class Listing(models.Model):
    # user = models.ForeignKey(User, on_delete = models.CASCADE)
    textbook = models.ForeignKey(Textbook, on_delete = models.CASCADE)
    class_object = models.ForeignKey(Class, on_delete = models.CASCADE)
    # condition = models.IntegerField(default = 0)
    condition = Field.choices[("likenew", "Like new"), ("verygood", "Very good"), ("good", "Good"), ("acceptable", "Acceptable")]
    picture = models.ImageField(upload_to = 'listing_images')
    comments = ArrayField(models.CharField(max_length = 500), blank = True)
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    hasBeenSoldFlag = models.BooleanField()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.textbook

    

