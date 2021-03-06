from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('<int:product_id>', views.detail, name='detail'),
    path('<int:product_id>/upvote', views.upvote, name='upvote'),
    path('<int:product_id>/deupvote', views.deupvote, name='deupvote'),
    path('<int:product_id>/upvotehome', views.upvotehome, name='upvotehome'),
    path('<int:product_id>/deupvotehome',
         views.deupvotehome, name='deupvotehome'),
    path('<int:product_id>/edit', views.edit, name='edit'),
    path('<int:product_id>/saveedit', views.saveedit, name='saveedit'),
    path('<int:product_id>/review', views.review, name='review'),
    path('<int:product_id>/<int:review_id>/like', views.like, name='like'),
    path('<int:product_id>/<int:review_id>/unlike', views.unlike, name='unlike'),
    path('<int:product_id>/<int:review_id>/dislike',
         views.dislike, name='dislike'),
    path('<int:product_id>/<int:review_id>/undislike',
         views.undislike, name='undislike'),
    path('<int:review_id>/deletereview',
         views.deletereview, name='deletereview'),
]
