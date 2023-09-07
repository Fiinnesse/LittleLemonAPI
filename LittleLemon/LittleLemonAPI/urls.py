from django.urls import path
from . import views

urlpatterns = [
    path('menu-item', views.ListViewMenuItem.as_view()),
    path('menu-item/<int:pk>', views.SingleMenuItemView.as_view()),
    path('categories', views.ListViewCategories.as_view()),
    path('categories/<int:pk', views.SingleCategoryView.as_view()),
]