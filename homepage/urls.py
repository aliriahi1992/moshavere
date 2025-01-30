from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('ask/<int:section>/', views.ask_question, name='ask_question'),
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),
    path('change-password/', views.change_password, name='change_password'),
]
