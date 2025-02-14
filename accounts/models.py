from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, full_name, password=None):
        if not mobile_number:
            raise ValueError("شماره موبایل باید وارد شود")
        user = self.model(mobile_number=mobile_number, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, full_name, password):
        user = self.create_user(mobile_number, full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    mobile_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # اضافه‌شده
    is_forget = models.BooleanField(default=False)  # اضافه‌شده
    is_webservice = models.BooleanField(default=False)  # اضافه‌شده
    webservice_from_who = models.IntegerField(default=1)  #عددی جهت مشخص شدن مشاور تخصیص یافته به وب سرویس
    webservice_origin = models.CharField(max_length=255,default="www")
    webservice_discount_code = models.CharField(max_length=255, null=True, blank=True)
    webservice_campaign_name = models.CharField(max_length=255, null=True, blank=True)
    webservice_total_request_limit = models.IntegerField(default=10000)
    webservice_user_request_limit = models.IntegerField(default=30)
    webservice_question_price = models.IntegerField(default=30000)
    balance = models.IntegerField(default=3)  #اعتبار اولیه با میزان پیش فرض 3 پرسش

    
    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.mobile_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
