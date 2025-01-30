from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import auth_page
from . import views


app_name = 'accounts'

urlpatterns = [
    path('auth/', auth_page, name='auth_page'),  # مسیر auth
    path('', auth_page, name='auth_page'),   # مسیر پیش‌فرض برای صفحه اصلی
    path('logout/', LogoutView.as_view(next_page='accounts:auth_page'), name='logout'),  # مسیر خروج از حساب کاربری با استفاده از نام فضای نامی
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]
