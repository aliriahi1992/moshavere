from django.contrib import admin
from .models import TransactionHistory
from .models import QuestionHistory
from import_export import resources
from import_export.admin import ExportMixin

# تعریف resource برای TransactionHistory
class TransactionHistoryResource(resources.ModelResource):
    class Meta:
        model = TransactionHistory
        fields = ('id', 'created_at', 'status', 'user_phone_number', 'user_full_name', 'orginal_price', 'amount', 'ref_id', 'discount_code', 'initial_credit', 'secondary_credit', 'user_os')

# تعریف resource برای QuestionHistory
class QuestionHistoryResource(resources.ModelResource):
    class Meta:
        model = QuestionHistory
        fields = ('id', 'created_at', 'status', 'user_phone_number', 'user_full_name', 'question', 'from_who', 'api_key_name', 'credit', 'user_os','webservice_user')

# ثبت TransactionHistory با قابلیت خروجی اکسل
@admin.register(TransactionHistory)
class TransactionHistoryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('status', 'user_full_name', 'user_phone_number', 'created_at', 'orginal_price', 'amount', 'discount_code', 'user_os')
    search_fields = ('user_full_name', 'user_phone_number', 'ref_id')
    resource_class = TransactionHistoryResource

# ثبت QuestionHistory با قابلیت خروجی اکسل
@admin.register(QuestionHistory)
class QuestionHistoryAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('status', 'user_full_name', 'user_phone_number', 'created_at', 'question', 'from_who', 'credit', 'user_os','webservice_user')
    search_fields = ('user_full_name', 'user_phone_number')
    resource_class = QuestionHistoryResource  
