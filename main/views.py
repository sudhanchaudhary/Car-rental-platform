import uuid
import hmac
import hashlib
import base64

from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Count,Prefetch
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg,Count
from cart.cart import Cart
from django.db.models import Avg
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

from .models import HeroProduct,Product,Category,SubCategory,Review,SiteReview
from account.models import Notification

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
    paginator=Paginator(product,3)
    page=request.GET.get('page')
    data=paginator.get_page(page)
    context={
        'category':category,
        'product':product,
        'data':data
    }
    if request.headers.get("HX-request"):
        return render(request,'main/product.html',context)
    return render(request,'main/category.html',context)

def review(request):
    see_all=request.GET.get('all')
    if see_all:
        review=SiteReview.objects.all()
    else:
        review=SiteReview.objects.all()[:2]
    if request.user.is_authenticated:
        if request.method == 'POST':
            SiteReview.objects.create(
                user=request.user,
                rating=request.POST.get('rating'),
                feedback=request.POST.get('feedback')
            )
            Notification.objects.create(user=request.user,title='Feedback submitted successfully')
            return redirect('review')
        
    return render(request,'main/review.html',{'review':review})

def host_guide(request):
    return render(request,'main/listycar.html')


@login_required(login_url='log_in')
def vehicle_detail(request, id):
    if request.user.profile.approved:
        
        product = get_object_or_404(Product, id=id)
        reviews = product.reviews.filter(rating__gte=3)
        if reviews.exists():
            avg_review = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        else:
            avg_review = 0

        review_count = reviews.count()
        existing = Review.objects.filter(user=request.user, product=product).first()
        show_all = request.GET.get('show_all')

        if show_all:
            reviews = reviews
        else:
            reviews = reviews[:1]
        if request.method == 'POST':
            Review.objects.create(
                user=request.user,
                product=product,
                rating=request.POST.get('rating'),
                feedback=request.POST.get('feedback')
            )
            Notification.objects.create(user=request.user,title=f'Reviewed the product {product.name}.')
            return redirect('vehicle_detail', id=product.id)
        
        context = {
            'product': product,
            'review': reviews,
            'avg_rating': round(avg_review),
            'existing': existing,
            'review_count': review_count,
            'show_all': show_all,
            'range':range(1,6)
            }

        return render(request, 'main/vehicle_detail.html', context)
    else:
        return redirect('profile')


"""
=====================================================================================
                                    cart
=====================================================================================
"""

@login_required(login_url="log_in")
def add_to_checkout(request, id):
    product = get_object_or_404(Product, id=id)

    request.session['checkout'] = {
        "product_id": product.id,
        "name": f"{product.brand} {product.model}",
        "price": float(product.price_per_day),
        "image": product.image.url,
        "days": 1
    }

    request.session.modified = True

    return redirect("checkout")

@login_required(login_url="log_in")
def update_checkout_days(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")

        item = request.session.get("checkout")

        if not item:
            return JsonResponse({"success": False})

        if action == "plus":
            item["days"] += 1

        elif action == "minus" and item["days"] > 1:
            item["days"] -= 1

        request.session["checkout"] = item
        request.session.modified = True

        return JsonResponse({
            "success": True,
            "days": item["days"]
        })

    return JsonResponse({"success": False})

def generate_signature(data, secret): 
    # signed_field_names must be included in the payload 
    signed_fields = data["signed_field_names"].split(",") 
     
    # Create message string in exact order 
    message = ",".join([f"{field}={data[field]}" for field in signed_fields]) 
    signature = hmac.new( 
        secret.encode("utf-8"), 
        message.encode("utf-8"), 
        hashlib.sha256 
    ).digest() 
     
    return base64.b64encode(signature).decode("utf-8")

@login_required(login_url="log_in")
def checkout(request):
    item = request.session.get('checkout')

    if not item:
        return redirect('home')

    total = item["price"] * item["days"]
    vat = total * 0.13
    product_code = "EPAYTEST" 
    secret_key = "8gBm/:&EnhH.1/q"
    data = {
        "item": item,
        "total": total,
        "vat": vat,
        "grand_total": total + vat,
        "amount": total, 
        "tax_amount": vat, 
        "total_amount": total + vat, 
        "transaction_uuid": str(uuid.uuid4()), 
        "product_code": product_code, 
        "product_service_charge": 0, 
        "product_delivery_charge": 0, 
        "success_url": "http://127.0.0.1:8000/payment/success/", 
        "failure_url": "http://127.0.0.1:8000/payment/failure/", 
        "signed_field_names": "total_amount,transaction_uuid,product_code",
    }
    data['signature']=generate_signature(data, secret_key)
    return render(request, 'main/cart.html', data)

