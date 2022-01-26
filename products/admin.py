from django.contrib import admin
from .models import Product, Like, Dislike, Review

# Register your models here.
admin.site.register(Product)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Review)