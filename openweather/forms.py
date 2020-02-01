from django import forms

## Forma za pretraživanje novih gradova. 

class SearchForm(forms.Form):
    name = forms.CharField(label='Naziv grada', max_length=100)
    