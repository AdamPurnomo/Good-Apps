from django.conf.urls import url
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Upvote
from django.utils import timezone
from django.db.models import Q
# Create your views here.


def home(request):
    products = Product.objects.order_by('-votes_total')
    return render(request, 'products/home.html', {'products': products})


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        upvote = Upvote.objects.get(
            Q(votedby=request.user) & Q(votedfor=product))
        upvote = True
    except Upvote.DoesNotExist:
        upvote = False
    return render(request, 'products/detail.html', {'product': product, 'upvote': upvote})


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


@login_required(login_url='/accounts/signup')
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


@login_required(login_url='/accounts/signup')
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


@login_required
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
