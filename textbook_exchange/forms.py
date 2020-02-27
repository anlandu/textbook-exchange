from django import forms

class SellForm(forms.Form):
    book_title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_author = forms.CharField(label='Author', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    isbn = forms.CharField(label='ISBN', widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_condition = forms.ChoiceField(label='Condition', choices=[("likenew", "Like new"), ("verygood", "Very good"), ("good", "Good"), ("acceptable", "Acceptable")], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), initial="likenew")
    price = forms.DecimalField(label='Price (USD)', min_value=0.0, max_value=400.0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    picture = forms.ImageField(label='Upload picture', widget=forms.FileInput(attrs={'class': 'form-control'}))
    comments = forms.CharField(label='Comments', required=False, max_length=300, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))

    def submit_listing(self):
        print(self.cleaned_data['book_name'] + " by " + self.cleaned_data['book_author'])


# from django.utils.translation import ugettext_lazy as _
# from django.forms import ModelForm, Textarea, TextInput, NumberInput, FileInput
# from .models import Listing
# 
# class SellForm(forms.ModelForm):
#     class Meta:
#         model = Listing
#         fields = ('textbook', 'class_object', 'condition_choices', 'picture', 'price', 'comments') #how to get foreignKey fields?
#         # https://stackoverflow.com/questions/21164798/django-modelform-with-foreign-key
#         # https://stackoverflow.com/questions/5708650/how-do-i-add-a-foreign-key-field-to-a-modelform-in-django

#         labels = {
#             'class_code': _('Class code'),
#             'class_title': _('Class title'),
#             'title': _('Title'),
#             'author': _('Author'),
#             'edition': _('Edition'),
#             'isbn': _('ISBN'),
#             'condition': _('Condition'),
#             'photo': _('Upload Photo'),
#             'price': _('Price'),
#             'comments': _('Comments'),
#             # cover_photo
#         }
#         widgets = {
#             'name': Textarea(attrs={'cols': 80, 'rows': 20}),
#             'isbn': NumberInput(attrs={'class': 'form-control'}),
#             'book_title': TextInput(attrs={'class': 'form-control'}),
#             'author': TextInput(attrs={'class': 'form-control'}),
#             # 'condition': ChoiceField(choices=[("likenew", "Like New"),("good", "Good"), ("acceptable", "Acceptable")], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
#             'price': NumberInput(attrs={'class': 'form-control'}),
#             'picture': FileInput(attrs={'class': 'form-control'}),
#             'comments': Textarea(attrs={'class': 'form-control', 'rows': '3'}),
#         }
#         # error_messages = {
#         #     'isbn': {
#         #         'max_length': _("This writer's name is too long."),
#         #     },
#         # }
