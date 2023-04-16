from django.http import  JsonResponse
from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import auth
import  json

def  home(request):
    products=Products.objects.filter(trending=1)
    return render (request, 'index.html',{"products":products})

def fav_view_page(request):
    if request.user.is_authenticated:
     fav=Favourite.objects.filter(user=request.user)
     return render(request,"fav.html",{"fav":fav})
    else:
     return redirect("/")
 
def cart_page(request):
  if request.user.is_authenticated:
    cart_page=Cart.objects.filter(user=request.user)
    return render(request,"card.html",{"cart":cart_page})
  else:
    return redirect("/")


def remove_fav(request,fid):
    item=Favourite.objects.get(id=fid)
    item.delete()
    return redirect("/fav_view_page")


def remove_cart(request,cid):
    cart_pageitem=Cart.objects.get(id=cid)
    cart_pageitem.delete()
    return redirect("/cart_page")



def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
       if request.user.is_authenticated:
           data=json.load(request)
           product_id=data['pid']
           product_status=Products.objects.get(id=product_id)
           if product_status:
               if  Favourite.objects.filter(user=request.user.id,product_id=product_id):
                 return JsonResponse({'status':'Product Already in Favourite'},status=200)
               else:
                 Favourite.objects.create(user=request.user,product_id=product_id)
                 return JsonResponse({'status':'Product Added to Favourite'},status=200)
      
       else:
           return JsonResponse({'status':'login to add to Favourite'},status=200)
        
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    



def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
       if request.user.is_authenticated:
           data=json.load(request)
           product_qty=data['product_qty']
           product_id=data['pid']
           product_status=Products.objects.get(id=product_id)
           if product_status:
               if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':' Product  Already in  Cart'},status=200)
               else:
                   if product_status.quantity >= product_qty:
                      Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                      return JsonResponse({'status':'Product  Added to Cart'},status=200)
                   else:
                      return JsonResponse({'status':'Product Stock not Available'},status=200)

       else:
           return JsonResponse({'status':'login to add to cart'},status=200)
        
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    

    
def logout_page(request):
  if request.user.is_authenticated:
     logout(request)
     messages.success(request,"Logged out Successfully")
  return redirect("/")

def  login_page(request):
    if request.user.is_authenticated:
          return redirect('home')
    else:
      if request.method == "POST":
        u = request.POST['username']
        p = request.POST['password']
        
        user = auth.authenticate(request,username=u,password=p)
        if user is not None:
            auth.login(request, user) 
            return redirect('home') 
        else:
            messages.error(request,'incorrect username or password')
            return redirect('login')
        
    return render (request, 'login.html')


def register(request):
    if request.method == "POST":
        u = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']
        
        user = User.objects.create(username=u,email=e,password=p)
        user.save()
        messages.success(request,'successfully registered please login')
        return redirect('login')
   
    return render(request,"register.html")
    

def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render (request,'collections.html',{"catagory":catagory})

def collectionsview(request,name):
    
    if(Catagory.objects.filter(name=name,status=0)):
       products=Products.objects.filter(catagory__name=name)
       return render(request,'products\index.html',{"products":products ,"category_name":name})
    else:
         messages.warning(request,"No Such Catagory Found")
         return redirect('collections')  
     
def products_details(request,cname,pname):
      if(Catagory.objects.filter(name=cname,status=0)):
       if(Products.objects.filter(name=pname,status=0)):
        products=Products.objects.filter(name=pname,status=0).first()
        return render(request,"products/products_details.html",{"products":products})
   
        
      else:
         messages.warning(request,"No Such Catagory Found")
         return redirect('collections')  
     
     
