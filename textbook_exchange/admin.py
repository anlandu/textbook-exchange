from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Textbook, Class, ProductListing, User, Cart, PendingTransaction

admin.site.register(Textbook)
admin.site.register(Class)
admin.site.register(ProductListing)
admin.site.register(User, UserAdmin)
admin.site.register(Cart)
admin.site.register(PendingTransaction)