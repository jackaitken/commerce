from django.forms import ModelForm
from .models import User, Listing, Bid, Comment

class CreateListing(ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'price', 'image', 'category'
        ]
