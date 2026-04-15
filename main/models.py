from django.db import models

# Create your models here.
class HeroProduct(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to='images',null=True,blank=True)
    desc=models.TextField()
    price=models.PositiveIntegerField()
    is_available=models.BooleanField(default=False)