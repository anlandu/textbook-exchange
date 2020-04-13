from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Textbook, Class, ProductListing, User, Cart, PendingTransaction

admin.site.register(Textbook)
admin.site.register(Class)
admin.site.register(User, UserAdmin)
admin.site.register(Cart)
admin.site.register(PendingTransaction)

class ProductListingAdmin(admin.ModelAdmin):
    readonly_fields = ('published_date', 'sold_date')

admin.site.register(ProductListing, ProductListingAdmin)
