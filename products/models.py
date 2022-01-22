from django.db import models
from django.contrib.auth.models import User

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
