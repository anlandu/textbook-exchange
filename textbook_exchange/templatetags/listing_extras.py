from django import template
register = template.Library()

@register.inclusion_tag('product_listing.html')
def show_product_listings(textbook_exchange): # is poll here supposed to be the model ProductListing?
    product_listings = textbook_exchange.product_listing_set.all() # what is polls.choice_set.all() replaced by?
    return {'product_listings': product_listings}


# @register.inclusion_tag('textbook_listing.html')
# def show_product_listings(textbook_exchange): # is poll here supposed to be the model ProductListing?
#     textbooks = textbook_exchange.textbook_set.all() # what is polls.choice_set.all() replaced by?
#     return {'textbooks': textbooks}