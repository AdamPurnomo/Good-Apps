from django.conf.urls import url
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Upvote, Review, Like, Dislike
from django.utils import timezone
from django.db.models import Q
import json
# Create your views here.


def home(request):
    products = Product.objects.order_by('-votes_total')
    upvoted = []
    for product in products:
        upvoted.append(False)

    if request.user.is_authenticated:
        i = 0
        for product in products:
            try:
                Upvote.objects.get(Q(votedby=request.user) &
                                   Q(votedfor=product))
                upvoted[i] = True
            except Upvote.DoesNotExist:
                pass
            i += 1
    return render(request, 'products/home.html', {'list': zip(products, upvoted)})


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    upvote = False
    try:
        reviews = Review.objects.filter(reviewee=product).order_by('-pub_date')
        reviewlikes = []
        likedbyuser = []
        dislikedbyuser = []
        reviewID = []
        for review in reviews:
            reviewID.append(review.id)
            numlikes = 0
            try:
                likes = Like.objects.filter(likedpost=review)
                numlikes = len(likes)

                if request.user.is_authenticated:
                    try:
                        likes.get(likedby=request.user)
                        likedbyuser.append(True)
                    except Like.DoesNotExist:
                        likedbyuser.append(False)
                else:
                    likedbyuser.append(False)
            except Like.DoesNotExist:
                pass

            numdislikes = 0
            try:
                dislikes = Dislike.objects.filter(dislikedpost=review)
                numdislikes = len(dislikes)

                if request.user.is_authenticated:
                    try:
                        dislikes.get(dislikedby=request.user)
                        dislikedbyuser.append(True)
                    except Dislike.DoesNotExist:
                        dislikedbyuser.append(False)
                else:
                    dislikedbyuser.append(False)
            except Dislike.DoesNotExist:
                pass

            reviewlikes.append(numlikes-numdislikes)
    except Review.DoesNotExist:
        pass

    # Next, bundle each review with its like and dislikes

    if request.user.is_authenticated:
        try:
            upvote = Upvote.objects.get(
                Q(votedby=request.user) & Q(votedfor=product))
            upvote = True
        except Upvote.DoesNotExist:
            pass
    userlikes = {'liked' : likedbyuser, 'disliked' : dislikedbyuser, 'reviewID': reviewID}
    return render(request, 'products/detail.html', {'product': product, 'upvote': upvote, 'userlikes': json.dumps(userlikes), 'reviewsbundle': zip(reviews, reviewlikes)})


@ login_required(login_url='/accounts/signup')
def review(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        if request.POST['body']:
            print("review object created")
            rev = Review()
            rev.reviewer = request.user
            rev.reviewee = product
            rev.body = request.POST['body']
            rev.pub_date = timezone.datetime.now()
            rev.save()
        return redirect('/products/' + str(product.id))


def edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/edit.html', {'product': product})


def saveedit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url']:
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.save()  # save data to database
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'You are required to fill all fields.'})

    else:
        return redirect('/products/' + str(product.id))


@ login_required(login_url='/accounts/signup')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()

        upvote = Upvote()
        upvote.votedby = request.user
        upvote.votedfor = product
        upvote.save()
        return redirect('/products/' + str(product.id))


def like(request, product_id, review_id):
    if request.user.is_authenticated and request.method == 'POST':
        like_increment = 0
        review = get_object_or_404(Review, pk=review_id)
        try:
            thumbdown = Dislike.objects.get(
                Q(dislikedpost=review) & Q(dislikedby=request.user))
            thumbdown.delete()
            like_increment += 1
        except Dislike.DoesNotExist:
            pass
        thumbup = Like(likedby=request.user, likedpost=review)
        thumbup.save()
        like_increment += 1
        data = {'like_increment': like_increment}
        return JsonResponse(data)


def dislike(request, product_id, review_id):
    if request.user.is_authenticated and request.method == 'POST':
        like_decrement = 0
        review = get_object_or_404(Review, pk=review_id)
        try:
            thumbup = Like.objects.get(
                Q(likedpost=review) & Q(likedby=request.user))
            thumbup.delete()
            like_decrement += 1
        except Like.DoesNotExist:
            pass
        thumbdown = Dislike(dislikedby=request.user, dislikedpost=review)
        thumbdown.save()
        like_decrement += 1
        data = {'like_decrement': like_decrement}
        return JsonResponse(data)


def unlike(request, product_id, review_id):
    if request.user.is_authenticated and request.method == 'POST':
        review = get_object_or_404(Review, pk=review_id)
        like_decrement = 0
        try:
            thumbup = Like.objects.get(
                Q(likedpost=review) & Q(likedby=request.user))
            thumbup.delete()
            like_decrement += 1
        except Like.DoesNotExist:
            pass
        data = {'like_decrement': like_decrement}
    return JsonResponse(data)

def undislike(request, product_id, review_id):
    if request.user.is_authenticated and request.method == 'POST':
        review = get_object_or_404(Review, pk=review_id)
        like_increment = 0
        try:
            thumbdown = Dislike.objects.get(
                Q(dislikedpost=review) & Q(dislikedby=request.user))
            thumbdown.delete()
            like_increment +=1
        except Dislike.DoesNotExist:
            pass
        data = {'like_increment': like_increment}
    return JsonResponse(data)


@ login_required(login_url='/accounts/signup')
def deupvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total -= 1
        product.save()

        upvote = Upvote.objects.get(
            Q(votedby=request.user) & Q(votedfor=product))
        upvote.delete()
        return redirect('/products/' + str(product.id))


@ login_required(login_url='/accounts/signup')
def upvotehome(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()

        upvote = Upvote()
        upvote.votedby = request.user
        upvote.votedfor = product
        upvote.save()
        return redirect('home')


@ login_required(login_url='/accounts/signup')
def deupvotehome(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total -= 1
        product.save()

        upvote = Upvote.objects.get(
            Q(votedby=request.user) & Q(votedfor=product))
        upvote.delete()
        return redirect('home')


@ login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()  # save data to database
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'You are required to fill all fields.'})

    else:
        return render(request, 'products/create.html')
