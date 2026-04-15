from django.shortcuts import render
from .models import HeroProduct

# Create your views here.
def home(request):
    hero=HeroProduct.objects.filter(is_available=True)
    context={
        'hero':hero,
    }
    return render(request,'main/home.html',context)