from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'requiredField'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'requiredField'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'requiredField'}))

class searchForm(forms.Form):
    query = forms.CharField(label= 'search', max_length= 50)