from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ["user", "full_name"]
    search_fields = ["user", "full_name"]
    list_filter = ["user", "full_name"]
    save_on_top = True


admin.site.register(UserProfile, UserProfileAdmin)