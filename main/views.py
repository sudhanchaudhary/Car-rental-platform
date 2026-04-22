from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Count,Prefetch
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import HeroProduct,Product,Category,SubCategory,Review

# Create your views here.
def home(request):
    hero=HeroProduct.objects.filter(is_available=True)
    context={
        'hero':hero,
    }
    return render(request,'main/home.html',context)

def category(request):
    category=Category.objects.annotate(sub_count=Count('subcategory')).\
        prefetch_related(Prefetch('subcategory_set',queryset=SubCategory.objects.annotate(product_count=Count('product'))))
    sub_id=request.GET.get('subcategory')
    if sub_id:
        product=Product.objects.filter(subcategory=sub_id)
    else:
        product=Product.objects.filter(approved=True)
    context={
        'category':category,
        'product':product
    }
    if request.headers.get("HX-request"):
        return render(request,'main/product.html',context)
    return render(request,'main/category.html',context)

def host_guide(request):
    return render(request,'main/listycar.html')

@login_required(login_url='log_in')
def vehicle_detail(request,id):
    product=get_object_or_404(Product,id=id)
    context={
        'product':product
    }
    return render(request,'main/vehicle_detail.html',context)