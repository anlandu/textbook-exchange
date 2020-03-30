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
    balance = models.DecimalField(max_digits=9, decimal_places=2)

    ACCOUNT_EMAIL_VERIFICATION = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

class Class(models.Model):
    class_term = models.CharField(max_length=200, default="")
    department = models.CharField(max_length=200) #e.g. CS
    course_code = models.IntegerField(default=0) #e.g. 1110
    section_number = models.CharField(max_length=10) #e.g. 001
    professor = models.CharField(max_length=200)
    class_info = models.TextField(max_length=200, primary_key=True) #e.g. CS1110
    
    @classmethod
    def create(cls, **kwargs):
        class_obj = cls.objects.create(
            class_term=kwargs['Term'],
            department=kwargs['Dept'],
            course_code=kwargs['Course'],
            section_number=kwargs['Sect'],
            professor=kwargs['Instructor'],
            class_info=kwargs['Dept']+kwargs['Course']+"-"+kwargs['Sect']
        )
        return class_obj

    def __str__(self):
        return self.class_info

class Textbook(models.Model):
    class_objects = models.ManyToManyField(Class) # on_delete for ManyToManyField?
    bookstore_isbn =  models.CharField(primary_key=True, max_length=200, default="")
    isbn13 = models.CharField(max_length=200, default="")
    isbn10 = models.CharField(max_length=200, default="")

    title = models.CharField(max_length=350, default="")
    author = models.CharField(max_length=200, default="")
    req_type = models.CharField(max_length=200, default="")
    cover_photo_url = models.CharField(max_length=400, default="")
    cover_photo = models.ImageField(upload_to='textbook_images')
    bookstore_new_price = models.FloatField(default=0, blank=True)
    bookstore_used_price = models.FloatField(default=0, blank=True)
    publisher = models.CharField(max_length=200, default="")
    date=models.CharField(max_length=200, default="")
    description = models.CharField(max_length=100000, default="")
    page_count = models.IntegerField(default=0, blank=True)
    google_rating = models.FloatField(default=0, blank=True)
    num_reviews = models.IntegerField(default=0, blank=True)

    @classmethod
    def create(cls, **kwargs):
        book = cls.objects.create(
            bookstore_isbn=kwargs['ISBN'],
            isbn13=kwargs['ISBN13'],
            isbn10=kwargs['ISBN10'],
            title=kwargs['Title'],
            author=kwargs['Author'],
            req_type=kwargs['Req Type'],
            cover_photo_url=kwargs['Image Links'],
            bookstore_new_price=float(kwargs['New'].replace('$', '').strip()),
            bookstore_used_price=float(kwargs['Used'].replace('$', '').strip()),
            publisher=kwargs['Publisher'],
            date=kwargs ['Publish Year'],
            description=kwargs['Description'],
            page_count=mkint(kwargs['Page Count']),
            google_rating=mkflt(kwargs['Google Rating']),
            num_reviews=mkint(kwargs['Number of Ratings'])
        )
        return book

    def __str__(self):
        textbook = '%s' % (self.title)
        return textbook.strip()

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # one cart per user
    subtotal = models.DecimalField(max_digits=6, decimal_places=2) # total without tax of books
    items = models.IntegerField() # number of items in cart

    def __str__(self):
        return str(self.items) + " items totaling $" + str(self.subtotal)

class ProductListing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    class_object = models.ManyToManyField(Class) # on_delete for ManyToManyField?
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True) # should prevent a product listing from being in multiple carts at once
    price = models.DecimalField(max_digits=7, decimal_places=2)
    condition = models.CharField(max_length=10)
    picture = models.ImageField(upload_to='listing_images')
    comments = models.CharField(max_length=500, blank=True)
    hasBeenSoldFlag = models.BooleanField(default=False)
    published_date = models.DateTimeField('date published', auto_now=True)

    def __str__(self):
        return str(self.textbook)

class PendingTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=9, decimal_places=2)
    date_transacted = models.DateTimeField(auto_now=True)
    date_settled = models.DateTimeField(auto_now=False)

    def __str__(self):
        return "Transaction for $" + str(self.balance) + " being settled on " + str(self.date_settled)
   
def mkflt(str_in):
    if str_in:
        return float(str_in)
    else:
        return 0

def mkint(str_in):
    if str_in:
        return int(str_in)
    else:
        return 0
