from django import forms

class SellForm(forms.Form):
    book_name = forms.CharField(label='Book Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    book_author = forms.CharField(label='Book Author', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    isbn = forms.IntegerField(label='ISBN', min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    book_condition = forms.ChoiceField(label='Book Condition', choices=[("likenew", "Like New"),("good", "Good"), ("acceptable", "Acceptable")], widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    price = forms.DecimalField(label='Price ($)', min_value=0.0, max_value=400.0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    picture = forms.ImageField(label='Picture of Book', widget=forms.FileInput(attrs={'class': 'form-control'}))
    comments = forms.CharField(label='Comments about Textbook', max_length=300, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))

    def submit_suggestion(self):
        print(self.cleaned_data['book_name'] + " by " + self.cleaned_data['book_author'])
