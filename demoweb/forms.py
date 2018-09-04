from django import forms

class LoginForm(forms.Form):
#    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'email@example.com'}))
    username = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs = {'class':'form-control','placeholder':'Password'}))
    remember_me = forms.BooleanField(required=False)
