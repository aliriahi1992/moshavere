from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('mobile_number', 'full_name','created_at','last_login' ,'login_counter', 'balance', 'is_staff', 'is_admin', 'is_active' ,'is_forget','is_webservice','webservice_from_who','webservice_origin','webservice_discount_code','webservice_campaign_name','webservice_total_request_limit','webservice_user_request_limit','webservice_question_price')  # اضافه کردن balance به list_display
    list_filter = ('is_staff', 'is_admin', 'is_active','is_webservice')
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('اطلاعات شخصی', {'fields': ('full_name', 'balance','created_at','last_login','login_counter')}),  # اضافه کردن balance به fieldsets
        ('دسترسی‌ها', {'fields': ('is_staff', 'is_admin', 'is_active','is_forget','is_webservice','webservice_from_who','webservice_origin','webservice_discount_code','webservice_campaign_name','webservice_total_request_limit','webservice_user_request_limit','webservice_question_price')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'full_name', 'password1', 'password2','created_at','last_login','login_counter', 'balance', 'is_staff', 'is_admin', 'is_active','is_forget','is_webservice','webservice_from_who','webservice_origin','webservice_discount_code','webservice_campaign_name','webservice_total_request_limit','webservice_user_request_limit','webservice_question_price'),
        }),
    )
    search_fields = ('mobile_number', 'full_name')
    ordering = ('mobile_number',)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)

