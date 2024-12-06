from django import forms

class BookSearchForm(forms.Form):
    book_name = forms.CharField(label='Book Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
