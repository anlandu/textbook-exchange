from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class SellForm(forms.Form):
    book_title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}))
    book_author = forms.CharField(label='Author', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}))
    isbn = forms.CharField(label='ISBN', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}))
    book_condition = forms.ChoiceField(label='Condition', choices=[("likenew", "Like new"), ("verygood", "Very good"), ("good", "Good"), ("acceptable", "Acceptable")], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), initial="likenew")
    price = forms.DecimalField(label='Price (USD)', min_value=0.0, max_digits=7, decimal_places=2, validators=[MaxValueValidator(500.00)], widget=forms.NumberInput(attrs={'class': 'form-control'}))
    picture = forms.ImageField(label='Upload picture', widget=forms.FileInput(attrs={'class': 'form-control'}))
    comments = forms.CharField(label='Comments', required=False, max_length=300, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))

    def submit_listing(self):
        print(self.cleaned_data['book_name'] + " by " + self.cleaned_data['book_author'])

class EditForm(forms.Form):
    price = forms.DecimalField(label='Price (USD)', min_value=0.0, max_digits=7, decimal_places=2, validators=[MaxValueValidator(500.00)], widget=forms.NumberInput(attrs={'class': 'form-label', 'placeholder': '{{post.price}}'}))
    book_condition = forms.ChoiceField(label='Condition', choices=[("likenew", "Like new"), ("verygood", "Very good"), ("good", "Good"), ("acceptable", "Acceptable")], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), initial="likenew")
    # picture = forms.ImageField(label='Upload picture', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    comments = forms.CharField(label='Comments', required=False, max_length=300, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
