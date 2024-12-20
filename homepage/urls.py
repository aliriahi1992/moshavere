from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('ask/<int:section>/', views.ask_question, name='ask_question'),
]
