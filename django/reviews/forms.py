from django.forms import ModelForm, Textarea
from reviews.models import Review, Wine, Address
from django import forms
from bootstrap3.tests import TestForm

class ContactForm(TestForm):
    pass

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 40, 'rows': 15}),
        }

class WineForm(ModelForm):
    class Meta:
        model = Wine
        fields = ['name']
        widgets = {
            'name': Textarea(attrs={'cols': 40, 'rows': 1}),
        }

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['addr']
        widgets = {
            'addr': Textarea(attrs={'cols': 40, 'rows': 1}),
        }

