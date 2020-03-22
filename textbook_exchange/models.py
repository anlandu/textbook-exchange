from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    username = models.CharField(_('username'), max_length=120)
    password = models.CharField(max_length=120)
    first_name = models.CharField(_('first name'), max_length=120, blank=True)
    last_name = models.CharField(_('last name'), max_length=120, blank=True)
    email = models.EmailField(_('email address'), primary_key=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    ACCOUNT_EMAIL_VERIFICATION = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

class Class(models.Model):
    subject = models.CharField(max_length=200)
    class_name = models.CharField(max_length=200)
    class_acronym = models.CharField(max_length=200)
    class_code = models.IntegerField(default=0, primary_key=True)
    section_number = models.CharField(max_length=10)
    professor = models.CharField(max_length=200)

    def __str__(self):
        class_info = '%s%s' % (self.subject, self.class_code)
        return class_info.strip()

class Textbook(models.Model):
    class_object = models.ManyToManyField(Class) # on_delete for ManyToManyField?
    isbn = models.IntegerField(primary_key=True)
    class_key = models.CharField(max_length=200)
    title = models.CharField(max_length=350)
    author = models.CharField(max_length=200)
    edition = models.CharField(max_length=200)
    cover_photo = models.ImageField(upload_to='textbook_images')
    
    def __str__(self):
        textbook = '%s, Edition %s' % (self.title, self.edition)
        return textbook.strip()

class ProductListing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    class_object = models.ManyToManyField(Class) # on_delete for ManyToManyField?
    
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # condition = [("likenew", "Like new"), ("verygood", "Very good"), ("good", "Good"), ("acceptable", "Acceptable")]
    # condition_choices = models.CharField(condition, default="likenew", max_length=10)
    condition = models.CharField(max_length=10)
    picture = models.ImageField(upload_to='listing_images')
    comments = models.CharField(max_length=500, blank=True)
    hasBeenSoldFlag = models.BooleanField(default=False)
    published_date = models.DateTimeField('date published', auto_now=True)

    def __str__(self):
        return str(self.textbook)