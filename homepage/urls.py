from django.urls import path
from . import views

app_name = 'homepage'  # نام اپلیکیشن

urlpatterns = [
    path('', views.homepage, name='homepage'),  # صفحه اصلی
    path('process-question/', views.process_question, name='process_question'),  # پردازش درخواست AJAX
]
