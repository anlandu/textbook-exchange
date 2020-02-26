from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone

# does every model need user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) ?

# Create your models here.
class User(AbstractUser):
    # username = models.CharField(_('username'), max_length = 30)
    # first_name = models.CharField(_('first name'), max_length = 30, blank = True)
    # last_name = models.CharField(_('last name'), max_length = 30, blank = True)
    # email = models.EmailField(_('email address'), blank = True)
    # is_staff = models.BooleanField(_('staff status'), default = False)
    # date_joined = models.DateTimeField(_('date joined'), default = timezone.now)

    # id = models.AutoField()
    username = models.CharField(_('username'), max_length=30)
    password = models.CharField(max_length=30)
    first_name = models.CharField(_('first name'), max_length=30, blank = True)
    last_name = models.CharField(_('last name'), max_length=30, blank = True)
    email = models.EmailField(_('email address'), primary_key=True, blank = True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password'] #add first and last name?

class Textbook(models.Model):
    class_object = models.ForeignKey(User, on_delete=models.CASCADE)
    isbn = models.IntegerField(primary_key=True)
    #An ISBN Check is going to be needed here
    class_key = models.CharField(max_length=200)
    title = models.CharField(max_length=350)
    author = models.CharField(max_length=200)
    edition = models.CharField(max_length=200)
    cover_photo = models.ImageField(upload_to='textbook_images')
    
    def __str__(self):
        textbook = '%s %s' % (self.title, self.edition)
        return textbook.strip()

class Class(models.Model):
    department = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    class_name = models.CharField(max_length=200)
    class_acronym = models.CharField(max_length=200)
    class_code = models.IntegerField(default=0, primary_key=True)
    section_number = models.CharField(max_length=10)
    professor = models.CharField(max_length=200)

    def __str__(self):
        class_info = '%s%s' % (self.subject, self.class_code)
        return class_info.strip()

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    class_object = models.ForeignKey(Class, on_delete=models.CASCADE)
    # condition = models.IntegerField(default = 0)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    condition = [("likenew", "Like new"), ("verygood", "Very good"), ("good", "Good"), ("acceptable", "Acceptable")]
    condition_choices = models.CharField(condition, default="likenew", max_length=10)
    picture = models.ImageField(upload_to='listing_images')
    # comments = ArrayField(models.CharField(max_length=500), blank=True)
    comments = models.CharField(max_length=500, blank=True)
    hasBeenSoldFlag = models.BooleanField()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.textbook

    

