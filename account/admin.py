from django.contrib import admin
from .models import Profile, Notification

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Profile.objects.get(id=obj.id)
            if not old_obj.is_approved and obj.is_approved:
                Notification.objects.create(
                    user=obj.user,
                    title="Your profile has been approved"
                )

        super().save_model(request, obj, form, change)