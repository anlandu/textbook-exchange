from django.contrib import admin
from .models import Textbook, Class, ProductListing

admin.site.register(Textbook)
admin.site.register(Class)
admin.site.register(ProductListing)

# Register your models here.
