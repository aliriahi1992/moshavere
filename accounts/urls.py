from django.urls import path
from .views import auth_page

app_name = 'accounts'

urlpatterns = [
    path('auth/', auth_page, name='auth_page'),  # مسیر auth
    path('', auth_page, name='auth_page'),   # مسیر پیش‌فرض برای صفحه اصلی
    path('logout/', LogoutView.as_view(next_page='/accounts/auth/'), name='logout'), # مسیر خروج از حساب کاربری
]