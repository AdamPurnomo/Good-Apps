from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField(upload_to='images/')
    pub_date = models.DateTimeField()
    body = models.TextField()
    url = models.TextField()
    votes_total = models.IntegerField(default=1)
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def summary(self):
        sumlist = self.body.split()[:50]
        summ = ' '.join(sumlist) + '.....'
        return summ

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class Upvote(models.Model):
    votedby = models.ForeignKey(User, on_delete=models.CASCADE)
    votedfor = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.votedby.username) + " upvoted for " + str(self.votedfor.title)


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewee = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.reviewer.username) + " 's review on " + str(self.reviewee.title)


class Like(models.Model):
    likedby = models.ForeignKey(User, on_delete=models.CASCADE)
    likedpost = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.likedby.username) + " likes " + str(self.likedpost.reviewer.username) + "'s on " + str(self.likedpost.reviewee.title)


class Dislike(models.Model):
    dislikedby = models.ForeignKey(User, on_delete=models.CASCADE)
    dislikedpost = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.dislikedby.username) + " dislikes " + str(self.dislikedpost.reviewer.username) + "'s on " + str(self.dislikedpost.reviewee.title)
