from django.shortcuts import render
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework import generics, filters

# Create your views here.

class ListViewMenuItem(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['price','inventory']
    search_fields = ['title', 'price', 'inventory']
    
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
class ListViewCategories(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['title']
    search_fields = ['title']
    
class SingleCategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer