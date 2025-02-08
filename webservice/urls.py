from django.urls import path
from . import views

app_name = 'webservice'

urlpatterns = [
    path('webservice/', views.webservice_chat_view, name='webservice_chat_view'),
]