from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required

from .models import Profile

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
                User.objects.create_user(first_name=f_name,last_name=l_name,username=username,email=email,password=password,is_active=False)
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

        messages.success(request, 'Profile updated successfully')
        return redirect('profile')

    return render(request, 'profile/profile_update.html')

@login_required(login_url='log_in')
def profile(request):
    data=Profile.objects.get(user=request.user)
    print(request.FILES)
    return render(request,'profile/profile.html',{'data':data})