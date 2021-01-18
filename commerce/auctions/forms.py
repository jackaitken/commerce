from django.forms import ModelForm
from django import forms
from .models import User, Listing, Bid, Comment

class CreateListing(ModelForm):
    class Meta:
        model = Listing

        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Enter a brief description of your product',
                                            'style':'red'})
        }

        fields = [
            'title', 'description', 'price', 'image', 'category'
        ]

class AddComment(ModelForm):
    class Meta:
        model = Comment

        widget = {
            'title': forms.TextInput(attrs={'placeholder':'Title'}),
            'comment': forms.Textarea(attrs={'placeholder':'Add a comment'})
        }

        fields = [
            'title', 'comment'
        ]