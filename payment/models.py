from django.db import models
from django.contrib.auth.models import User
from main.models import Product
from datetime import timedelta

# Create your models here.
class Transaction(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    transaction_code=models.CharField(max_length=200)
    transaction_uuid=models.CharField(max_length=200)
    product_code=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
    total_amount=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    transaction_code=models.CharField(max_length=200)
    product_code=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
    total_amount=models.CharField(max_length=200)
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE,related_name='item')
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    price=models.CharField(max_length=20)
    quantity=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    booked_till = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.created_at and self.quantity:
            self.booked_till = self.created_at + timedelta(days=self.quantity)
        super().save(*args, **kwargs)