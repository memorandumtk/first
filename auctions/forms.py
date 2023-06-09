# forms.py
# from django import forms
from django.forms import ModelForm
from django.forms import IntegerField
from django.forms import NumberInput
from .models import Listing
from .models import Category
from .models import Bidmodel, Comment
from django import forms

# Create form "ListingForm" from Listing model   
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image", "category"]

class BidForm(ModelForm):
    # current_bid = forms.IntegerField(label="Your website", widget=NumberInput)
    class Meta:
        model = Bidmodel
        fields = ["current_bid"]

class CategoryForm(ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Cat something...",
                "class": "textarea is-success is-medium",
            }
        ),
        label="",
    )
        
    class Meta:
        model = Category
        fields = ["name"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["commentmessage"]