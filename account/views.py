from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

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
    return render(request,'auth/log_in.html')

def profile_update(request):
    return render(request, 'profile/profile_update.html')

def dashboard(request):
    return render(request,'profile/dashboard.html')

def profile(request):
    return render(request,'profile/profile.html')