from django.contrib import admin
from .models import HeroProduct,Category,SubCategory,Product,ProductImage,Review

# Register your models here.
admin.site.register(HeroProduct)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Review)

class ProductAdminImage(admin.TabularInline):
    model=ProductImage
    extra=2
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['model','price_per_day','approved']
    inlines=[ProductAdminImage]