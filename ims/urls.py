from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('accounts/', include('registration.backends.simple.urls')),
    path('list_items/', list_items, name="list_items"),
    path('list_history/', list_history, name="list_history"),
    path('add_items/', add_items, name="add_items"),
    path('update_items/<str:pk>', update_items, name="update_items"),
    path('delete_items/<str:pk>', delete_items, name="delete_items"),
    path('stock_detail/<str:pk>', stock_detail, name="stock_detail"),
    path('issue_items/<str:pk>', issue_items, name="issue_items"),
    path('receive_items/<str:pk>', receive_items, name="receive_items"),
    path('reorder_level/<str:pk>', reorder_level, name="reorder_level"),
    path('inventory_overview/', inventory_overview, name='inventory_overview'),
    path('inventory_trend_analysis/', inventory_trend_analysis,
         name='inventory_trend_analysis'),
    path('category_analysis/', category_analysis, name='category_analysis'),
    path('stock_movement_analysis/', stock_movement_analysis,
         name='stock_movement_analysis'),
    path('reorder_level_monitoring/', reorder_level_monitoring,
         name='reorder_level_monitoring'),
]
