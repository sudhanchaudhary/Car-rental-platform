from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HeroProduct(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to='images',null=True,blank=True)
    desc=models.TextField()
    price=models.PositiveIntegerField()
    is_available=models.BooleanField(default=False)
    
class Category(models.Model):
    title=models.CharField(max_length=200)
    def __str__(self):
        return self.title
    
class SubCategory(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
class Product(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name='owner')
    plate=models.CharField(max_length=100,default='1111')
    model=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory=models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    seats=models.IntegerField()
    milage=models.CharField(max_length=200)
    desc=models.TextField()
    make=models.IntegerField(null=True,blank=True)
    price_per_day=models.DecimalField(max_digits=10,decimal_places=2)
    bimg_number=models.ImageField(upload_to='bluebook',null=True,blank=True)
    bimg_detail=models.ImageField(upload_to='bluebook',null=True,blank=True)
    bimg_owner=models.ImageField(upload_to='bluebook',null=True,blank=True)
    image=models.ImageField(upload_to='product')
    created_at=models.DateTimeField(auto_now_add=True)
    is_available=models.BooleanField(default=True)
    approved=models.BooleanField(default=False)
    def __str__(self):
        return self.model
    @property
    def name(self):
        return f"{self.brand} {self.model}"
    @property
    def price(self):
        return self.price_per_day
    
class ProductImage(models.Model):
    image=models.ImageField(upload_to='Product_image',null=True,blank=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE,related_name='images')
    def __str__(self):
        return self.product.model

class Review(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE,related_name='reviews')
    rating=models.PositiveSmallIntegerField()
    feedback=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    
    