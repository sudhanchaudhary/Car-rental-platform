from django.contrib import admin
from django.utils.html import format_html
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
    list_display=['model','plate','price_per_day','b_number','b_detail','b_owner','approved']
    list_display_links = ['model']
    list_editable = ['approved']
    inlines=[ProductAdminImage]
    def b_number(self,obj):
        if obj.bimg_number:
            return format_html('<img src="{}" height="100px" width="130px">',obj.bimg_number.url)
    def b_detail(self,obj):
        if obj.bimg_detail:
            return format_html('<img src="{}" height="100px" width="130px">',obj.bimg_detail.url)
    def b_owner(self,obj):
        if obj.bimg_owner:
            return format_html('<img src="{}" height="100px" width="130px">',obj.bimg_owner.url)
            
    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Product.objects.get(id=obj.id)

            if not old_obj.approved and obj.approved:
                Notification.objects.create(
                    user=obj.owner,
                    title="Your vehicle has been approved"
                )

        super().save_model(request, obj, form, change)


    