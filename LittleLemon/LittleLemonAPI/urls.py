from django.urls import path, include
from . import views

urlpatterns = [
    path('menu-items', views.ListViewMenuItem.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('categories', views.ListViewCategories.as_view()),
    path('categories/<int:pk>', views.SingleCategoryView.as_view()),
    path('secret', views.secret),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]