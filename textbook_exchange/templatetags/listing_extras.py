from django import template
register = template.Library()

# You can pass arguments to your custom tag, process them a bit in Python, then bounce back to a template. 
# Direct inclusion only works for fragments that don't depend on the surrounding context.

@register.inclusion_tag('product_listing.html')
def show_product_listings(textbook_exchange):
    product_listings = textbook_exchange.product_listing_set.all() # what is polls.choice_set.all() replaced by?
    return {'product_listings': product_listings}
