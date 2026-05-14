from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

from main.models import Product,ProductImage,Category,SubCategory
from payment.models import Order,OrderItem,Transaction
from .models import Profile,Notification

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        f_name=request.POST.get('f_name')
        l_name=request.POST.get('l_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request,"Username already exists!!!")
                return redirect('sign_up')
            if User.objects.filter(email=email).exists():
                messages.error(request,"Email already used!!!")
                return redirect('sign_up')
            try:
                validate_password(password)
                User.objects.create_user(first_name=f_name,last_name=l_name,username=username,email=email,password=password)
                
                messages.success(request,'Please complete your profile to start booking.')
                return redirect('log_in')
            except ValueError as a:
                messages.error(request,a)
                return redirect('sign_up')
        else:
            messages.error(request,"password and cpassword doesn't match")
    return render(request,'auth/sign_up.html')

def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        user = authenticate(request, username=username, password=password)
        print("USER:", user)
        if user is not None:
            login(request, user)
            if remember:
                request.session.set_expiry(3600)  
            else:
                request.session.set_expiry(0) 
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('log_in')
    return render(request, 'auth/log_in.html')

@login_required(login_url='log_in')
def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def change_password(request):
    user = request.user

    if request.method == 'POST':
        opassword = request.POST.get('old_password')
        npassword = request.POST.get('new_password')
        cnpassword = request.POST.get('c_new_password')

        if not user.check_password(opassword):
            messages.error(request, 'Old password is incorrect')
            return redirect('pchange')

        if npassword != cnpassword:
            messages.error(request, 'New password and Confirm password do not match')
            return redirect('pchange')

        user.set_password(npassword)
        user.save()
        Notification.objects.create(user=request.user,title="Password changed successfully")

        update_session_auth_hash(request, user)

        messages.success(request, 'Password changed successfully')
        return redirect('profile')
    return render(request,'auth/change_password.html')

@login_required(login_url='log_in')
def profile_update(request):
    if request.method == 'POST':
        profile, created = Profile.objects.get_or_create(user=request.user)

        profile.profilepic = request.FILES.get('profile_pic')
        profile.fname = request.POST.get('fname')
        profile.lname = request.POST.get('lname')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.gender = request.POST.get('gender')
        profile.account_type = request.POST.get('actype')
        profile.citizen = request.POST.get('idnumber')
        profile.licence = request.POST.get('lnumber')
        profile.citizenfront = request.FILES.get('id_front')
        profile.citizenback = request.FILES.get('id_back')
        profile.licencefront = request.FILES.get('lfront')
        profile.licenceback = request.FILES.get('lback')
        profile.approved = False

        profile.save()
        Notification.objects.create(user=request.user,title="Profile updated successfully")
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')

    return render(request, 'profile/profile_update.html')

@login_required(login_url='log_in')
def profile(request):
    data, created = Profile.objects.get_or_create(user=request.user)
    return render(request,'profile/profile.html',{'data':data})

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
            Notification.objects.create(user=request.user,title="Vehicle added successfully")
            return redirect('listing')
        return render(request, 'profile/listing.html')
    messages.error(request, "Access denied. Host account needed.")
    return redirect('home')

@login_required(login_url='log_in')
def mylisting(request):
    if request.user.profile.account_type == 'host':
        data=Product.objects.filter(owner=request.user)
        del_id=request.GET.get('del')
        if del_id:
            product=Product.objects.get(id=del_id)
            product.delete()
            Notification.objects.create(user=request.user,title="Product deleted successfully")
            return redirect('mylisting')
        return render(request,'profile/mylisting.html',{'data':data})
    else:
        return redirect('profile')
    
@login_required(login_url='log_in')
def myearning(request):
    if request.user.profile.account_type == 'host':
        total_earning = OrderItem.objects.filter(
        product__owner=request.user).aggregate(total=Sum(ExpressionWrapper(F('price') * F('quantity'),output_field=DecimalField())))['total'] or 0
        booking_days=OrderItem.objects.filter(product__owner=request.user).aggregate(days=Sum('quantity'))['days'] or 0
        context={
            'my_earning':total_earning,
            'days':booking_days
        }
        return render(request, 'profile/myearning.html',context)
    
@login_required(login_url='log_in')
def history(request):
    if request.user.profile.account_type == 'renter':
        data = Order.objects.filter(user=request.user).prefetch_related('item__product')
        return render(request, 'profile/history.html',{'data':data})
    
@login_required(login_url='log_in')
def notification(request):
    data=Notification.objects.filter(user=request.user)[::-1]
    return render(request,'profile/notification.html',{'data':data})

@login_required(login_url='log_in')
def stats(request):
    if request.user.is_superuser:
        total = Transaction.objects.aggregate(total_amount=Sum('total_amount'))['total_amount']
        v_total=OrderItem.objects.aggregate(v_total=Sum('product'))['v_total']
        d_total=OrderItem.objects.aggregate(d_total=Sum('quantity'))['d_total']
        t_all=request.GET.get('t_all')
        p_all=request.GET.get('p_all')
        v_all=request.GET.get('v_all')
        if t_all:
            transaction=Transaction.objects.all()[::-1]
        else:
            transaction=Transaction.objects.all()[:5][::-1]
        if p_all:
            profile=Profile.objects.filter(approved=False)
        else:
            profile=Profile.objects.filter(approved=False)[:5]
        if v_all:
            vehicle=Product.objects.filter(approved=False)
        else:
            vehicle=Product.objects.filter(approved=False)[:5]
            
        print(transaction)
        context={
            'transaction':transaction,
            'profile':profile,
            'vehicle':vehicle,
            'total':total,
            'v_total':v_total,
            'd_total':d_total,
        }
        return render(request,'profile/stats.html',context)
    else:
        return redirect('profile')