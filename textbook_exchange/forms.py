from django import forms
import requests
import json

class SellForm(forms.Form):
    book_title = forms.CharField(label='Title', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}))
    book_author = forms.CharField(label='Author', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}))
    isbn = forms.CharField(label='ISBN', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}))
    book_condition = forms.ChoiceField(label='Condition', choices=[("likenew", "Like new"), ("verygood", "Very good"), ("good", "Good"), ("acceptable", "Acceptable")], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), initial="likenew")
    price = forms.DecimalField(label='Price (USD)', min_value=0.0, max_value=1000.0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    picture = forms.ImageField(label='Upload picture', widget=forms.FileInput(attrs={'class': 'form-control'}))
    comments = forms.CharField(label='Comments', required=False, max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))

class ContactForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Message', max_length=5000, widget=forms.Textarea(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Reply Email Address", widget=forms.EmailInput(attrs={'class': 'form-control'}))