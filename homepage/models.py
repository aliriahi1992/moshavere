from django.db import models

class TransactionHistory(models.Model):
    created_at = models.DateTimeField()
    status = models.CharField(max_length=255, default='NOK')
    user_phone_number = models.CharField(max_length=11)
    user_full_name = models.CharField(max_length=255)
    orginal_price = models.IntegerField()
    amount = models.IntegerField()
    ref_id = models.CharField(max_length=255 , blank=True, null=True)
    discount_code = models.CharField(max_length=255, blank=True, null=True)
    initial_credit = models.IntegerField()
    secondary_credit = models.IntegerField()
    user_os = models.CharField(max_length=255)

    def __str__(self):
        return f"Transaction {self.ref_id} for {self.user_full_name}"

