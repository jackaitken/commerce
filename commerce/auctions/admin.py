from django.contrib import admin

from .models import User, Comment, Bid, Listing, Watchlist

# Register your models here.

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Watchlist)
