from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('mobile_number', 'full_name', 'is_staff', 'is_admin', 'is_active')
    list_filter = ('is_staff', 'is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('اطلاعات شخصی', {'fields': ('full_name',)}),
        ('دسترسی‌ها', {'fields': ('is_staff', 'is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'full_name', 'password1', 'password2', 'is_staff', 'is_admin', 'is_active'),
        }),
    )
    search_fields = ('mobile_number', 'full_name')
    ordering = ('mobile_number',)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)
