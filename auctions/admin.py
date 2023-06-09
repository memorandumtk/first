from django.contrib import admin

from .models import Listing, Category, User, Watchlist, Comment, Bidmodel


# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_bid")
    

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Bidmodel)
