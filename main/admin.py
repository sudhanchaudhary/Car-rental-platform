from django.contrib import admin
from .models import HeroProduct,Category,SubCategory,Product,ProductImage,Review
from account.models import Notification
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
    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Product.objects.get(id=obj.id)

            if not old_obj.approved and obj.approved:
                Notification.objects.create(
                    user=obj.owner,
                    title="Your vehicle has been approved"
                )

        super().save_model(request, obj, form, change)


    