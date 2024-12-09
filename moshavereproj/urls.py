from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('accounts.urls')),  # مسیر پیش‌فرض به اپ accounts
    path('homepage/', include('homepage.urls')),  # مسیر اپ homepage
    path('admin/', admin.site.urls),  # مسیر ادمین
]