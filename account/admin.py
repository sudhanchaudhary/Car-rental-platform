from django.contrib import admin
from .models import Profile, Notification
from django.utils.html import format_html

admin.site.site_header='RentalHub'
admin.site.site_title='RentalHub'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['fname','lname','citizen','display_citizenfront','display_citizenback','approved']
    list_display_links = ['fname']
    list_editable = ['approved']
    def display_citizenfront(self,obj):
        if obj.citizenfront:
            return format_html('<img src="{}" height="100px" width="130px" >',obj.citizenfront.url)
        
    def display_citizenback(self,obj):
        if obj.citizenback:
            return format_html('<img src="{}" height="100px" width="130px" >',obj.citizenback.url)

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Profile.objects.get(id=obj.id)
            if not old_obj.is_approved and obj.is_approved:
                Notification.objects.create(
                    user=obj.user,
                    title="Your profile has been approved"
                )

        super().save_model(request, obj, form, change)