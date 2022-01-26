from django.contrib import admin
from .models import Product, Like, Dislike, Review, Upvote

# Register your models here.
admin.site.register(Product)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Review)
admin.site.register(Upvote)