from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.ListViewMenuItem.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('categories', views.ListViewCategories.as_view()),
    path('categories/<int:pk', views.SingleCategoryView.as_view()),
]