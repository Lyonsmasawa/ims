from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('list_items/', list_items, name="list_items"),
    path('add_items/', add_items, name="add_items"),
]
