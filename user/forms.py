from django import forms


class ProfileForm(forms.Form):
    fname=forms.CharField()
    lname=forms.CharField()
    email=forms.EmailField()
    image=forms.ImageField(required=False)
    about=forms.CharField()
    gender=forms.CharField(max_length=1)
