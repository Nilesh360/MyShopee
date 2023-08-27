from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Product,Category,User,cart
from .forms import ProductForm
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.decorators import api_view,throttle_classes,action,APIView
from .serializers import CategorySerializer
import chatbot

# Create your views here.

def home(request):
    products = Product.objects.all()
    category = Category.objects.all()
    carts = cart.objects.all()
 #   if request.user.is_authenticated:
  #      carts = request.user.cart_set.all()
    context={'products':products,'category':category,'carts':carts}
    return render(request,'base/home.html',context)

def ProductView(request,pk):
    product = Product.objects.get(id=pk)
    context={'product':product}
    response =  render(request,'base/Product.html',context)
    return response

@login_required(login_url='login')
def updateProduct(request,pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method=='POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/create_update_product.html',context)

@login_required(login_url='login')
def deleteProduct(request,pk):
    product = Product.objects.get(id=pk)
    if request.method=='POST':
        product.delete()
        return redirect('home')
    context = {'obj':product}
    return render(request,'base/delete_product.html',context)

@login_required(login_url='login')
def addProduct(request):
    form = ProductForm()
    if request.method=='POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/create_update_product.html',context)

def navbar(request):
        categories = Category.objects.all()
        return {
            'categories': categories,
            'chatbot':chatbot,
        }


#---------------------------------->Class based views <--------------------------------------

class registerPage(APIView):
    def post(self,request):
        page='register'
        form = UserCreationForm()
        if request.method=='POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username
                user.save()
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"An error occurred during registration")
                return self.get(request)

    def get(self,request):
        page='register'
        form = UserCreationForm()
        context = {'page':page,'form':form}
        return render(request,'base/login_register.html',context)
    

class AddtoCart(APIView):
    @method_decorator(login_required(login_url='login'))
    def get(self,request,pk):
        user = request.user
        product = Product.objects.get(id=pk)
        chk = cart.objects.filter(user = user , product=product)
        if chk.count()==0:
            cartProduct = cart.objects.create(
                user = user,
                product=product
            )
        return redirect('base:cart-product')
    
class logoutUser(APIView):
    @method_decorator(login_required(login_url='login'))
    def get(self,request):
        logout(request)
        request.session.flush()
        response = redirect('home')
        response.delete_cookie('csrftoken')
        return response

class LoginPage(APIView):
    throttle_classes = [AnonRateThrottle]
    def post(self,request):
        page='login'
        if request.user.is_authenticated:
            return redirect('home')
        if request.method=='POST':
            #print(request.COOKIES.get('csrftoken'))
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = User.objects.get(username=username)
                user = authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user)
                    return redirect('home')
                else:
                    messages.error(request,'Username or password does not exists')
                    return self.get(request)
            except:
                messages.error(request,'User does not exists')
                return self.get(request)
            
    def get(self,request):
        page='login'
        context={'page':page}
        return render(request,'base/login_register.html',context)
    
class SearchedProduct(APIView):
    category = Category.objects.all()
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    def get(self,request):
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        filter_products = self.get_queryset(Product,q)        
        search_param = q
        #serialized = CategorySerializer(self.category,many=True)
        #print(serialized.data)
        paginator = Paginator(filter_products, 10)   #10 search item on single page
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context={'filter_products':filter_products,'category':self.category,'page': page,'search_param':search_param}
        response= render(request,'base/filtered_product.html',context)
        #response.set_cookie('key1',['val1','val2'])
        #response.delete_cookie('key1')
        return response
    
    def get_queryset(self,Product,key):
        filter_products = Product.objects.filter(
            Q(name__icontains=key) |
            Q(description__icontains=key) |
            Q(category__name__icontains=key)
        )
        return filter_products
    
class CartView(APIView):
    @method_decorator(login_required(login_url='login'))
    def get(self,request):
        cartItem = request.user.cart_set.all()
        sum_of_cart_amount = 0
        for item in cartItem:
            sum_of_cart_amount = sum_of_cart_amount + item.product.price
        context={'cartItem':cartItem,'sum_of_cart_amount':sum_of_cart_amount}
        return render(request,'base/ProductCart.html',context)

