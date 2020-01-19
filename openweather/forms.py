from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(label='Naziv grada', max_length=100)