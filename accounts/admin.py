from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('mobile_number', 'full_name', 'balance', 'is_staff', 'is_admin', 'is_active' ,'is_forget','is_webservice','webservice_from_who','webservice_origin')  # اضافه کردن balance به list_display
    list_filter = ('is_staff', 'is_admin', 'is_active','is_webservice')
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('اطلاعات شخصی', {'fields': ('full_name', 'balance')}),  # اضافه کردن balance به fieldsets
        ('دسترسی‌ها', {'fields': ('is_staff', 'is_admin', 'is_active','is_forget','is_webservice','webservice_from_who','webservice_origin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'full_name', 'password1', 'password2', 'balance', 'is_staff', 'is_admin', 'is_active','is_forget','is_webservice','webservice_from_who','webservice_origin'),
        }),
    )
    search_fields = ('mobile_number', 'full_name')
    ordering = ('mobile_number',)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)

