from django.contrib import admin
from .models import TransactionHistory
from .models import QuestionHistory

@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('status', 'user_full_name', 'user_phone_number', 'created_at', 'orginal_price', 'amount' , 'discount_code' , 'user_os')
    search_fields = ('user_full_name', 'user_phone_number', 'ref_id')

@admin.register(QuestionHistory)
class QuestionHistoryAdmin(admin.ModelAdmin):
    list_display = ('status', 'user_full_name', 'user_phone_number', 'created_at', 'question', 'from_who' , 'credit' , 'user_os')
    search_fields = ('user_full_name', 'user_phone_number')    
