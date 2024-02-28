from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('list_items/', list_items, name="list_items"),
    path('add_items/', add_items, name="add_items"),
    path('update_items/<str:pk>', update_items, name="update_items"),
    path('delete_items/<str:pk>', delete_items, name="delete_items"),
    path('stock_detail/<str:pk>', stock_detail, name="stock_detail"),
    path('issue_items/<str:pk>', issue_items, name="issue_items"),
    path('receive_items/<str:pk>', receive_items, name="receive_items"),
]
