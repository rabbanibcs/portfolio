from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from user.models import User
PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
    ('C', 'Cash'),
)
ADD_CHOICES = (
    ('D', 'Default'),
    ('N', 'New'),
)



class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    # zip = forms.CharField(required=False)
    shipping_default = forms.ChoiceField(widget=forms.RadioSelect, choices=ADD_CHOICES)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        # fields = UserCreationForm.Meta.fields + ('first_name','last_name')
