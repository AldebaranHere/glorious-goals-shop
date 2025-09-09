from django.urls import path
from main.views import show_details

app_name = 'main'

urlpatterns = [
    path('', show_details, name='show_main'),
]