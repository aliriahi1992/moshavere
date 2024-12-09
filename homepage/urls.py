from django.urls import path
from . import views


app_name = 'homepage'  # این خط باید حتماً وجود داشته باشد


urlpatterns = [
    path('', views.homepage, name='homepage'),  # صفحه اصلی
]