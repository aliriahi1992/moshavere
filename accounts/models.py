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
    balance = models.IntegerField(default=5000)  # فیلد شارژ اولیه با مقدار پیش‌فرض 5000

    
    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.mobile_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
