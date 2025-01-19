from django.contrib import admin
from .models import TransactionHistory

@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('status', 'user_full_name', 'user_phone_number', 'created_at', 'orginal_price', 'amount' , 'discount_code' , 'user_os')
    search_fields = ('user_full_name', 'user_phone_number', 'ref_id')

# یا می‌تونی از این روش استفاده کنی
# admin.site.register(TransactionHistory, TransactionHistoryAdmin)

