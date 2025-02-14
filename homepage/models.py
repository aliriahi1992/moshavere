from django.db import models

class TransactionHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
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
    webservice_question_price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.ref_id} for {self.user_full_name}"


class QuestionHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default='None')
    user_phone_number = models.CharField(max_length=11)
    user_full_name = models.CharField(max_length=255)
    question = models.CharField(max_length=255, default='')
    from_who = models.CharField(max_length=255, default='')
    api_key_name = models.CharField(max_length=255, default='')
    credit = models.IntegerField()
    user_os = models.CharField(max_length=255)
    webservice_user = models.CharField(max_length=255, default='user')
    webservice_discount_code = models.CharField(max_length=255, null=True, blank=True)
    webservice_campaign_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user_full_name} - {self.status}"