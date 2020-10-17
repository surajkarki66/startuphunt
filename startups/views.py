from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone

def home(request):

    products = Product.objects
    return render(request, 'startups/home.html',{'products':products})

@login_required(login_url="/accounts/signup")
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
            product.save()
            return redirect('/startups/' + str(product.id))
        else:
            return render(request, 'startups/create.html',{'error':'All fields are required.'})
    else:
        return render(request, 'startups/create.html')


def detail(request,startup_id):
	product = get_object_or_404(Product,pk=startup_id)
	return render(request,'startups/detail.html',{'product':product})



@login_required(login_url="/accounts/signup")
def upvote(request, startup_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=startup_id)
        product.votes_total += 1
        product.save()
        return redirect('/startups/' + str(product.id))
