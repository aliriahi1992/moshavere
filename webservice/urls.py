from django.urls import path
from . import views

app_name = 'webservice'

urlpatterns = [
    path('ask/', views.webservice_chat_view, name='webservice_chat_view'),
    path('', views.homepage, name='homepage'),  # مسیر index برای نمایش صفحه webservice
    path('user-questions/', views.user_questions, name='user_questions'),
]