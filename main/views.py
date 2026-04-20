from django.shortcuts import render,redirect
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
def listing(request):
    profile = request.user.profile
    if profile.approved and profile.account_type == "host":
        
        if request.method == "POST":
            category=request.POST.get('category')
            subcategory=request.POST.get('subcategory')
            is_available=request.POST.get('available') == 'on'
            cate_instance=Category.objects.get(title=category)
            subcate_instance=SubCategory.objects.get(title=subcategory)
            Product.objects.create(
                owner=request.user,
                plate=request.POST.get('plate_number'),
                image=request.FILES.get('img'),
                brand=request.POST.get('brand'),
                model=request.POST.get('model'),
                category=cate_instance,
                subcategory=subcate_instance,
                seats=request.POST.get('seat'),
                milage=request.POST.get('milage'),
                price_per_day=request.POST.get('price'),
                make=request.POST.get('make'),
                desc=request.POST.get('desc'),
                is_available=is_available,
                bimg_number=request.FILES.get('number_image'),
                bimg_detail=request.FILES.get('detail_image'),
                bimg_owner=request.FILES.get('owner_image'),
                approved=False
                )
            return redirect('listing')
        return render(request, 'main/listing.html')
    messages.error(request, "Access denied. Host account needed.")
    return redirect('home')