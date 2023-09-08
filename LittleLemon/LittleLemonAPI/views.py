from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer, UserListSerializer
from rest_framework import generics, filters, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User, Group
from .permissions import AdminOrReadOnly





# Create your views here.
class ListViewMenuItem(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all().order_by('-featured')
    serializer_class = MenuItemSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['price','inventory','category']
    search_fields = ['title', 'price', 'inventory','category']
    
    
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [AdminOrReadOnly]
    
class ListViewCategories(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['title']
    search_fields = ['title']
    
class SingleCategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@permission_classes([IsAdminUser])    
class ManagerListView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserListSerializer

    def post(self, request, *args, **kwargs):
        if request.data == {}:
            return Response({'message':'add username to body'})
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Manager")
            managers.user_set.add(user)
            return Response({"message": 'Added user to Manager Group'}, status.HTTP_201_CREATED)
        return Response({'message': 'add username to value field'}, status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request, *args, **kwargs):
        if request.data == {}:
            return Response({'message':'add username to body'})
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Manager")
            managers.user_set.remove(user)
            return Response({'message': 'Removed user from Manager Group'}, status.HTTP_200_OK) 
        return Response({'message': 'add username to value field'}, status.HTTP_400_BAD_REQUEST)

    
@permission_classes([IsAdminUser])    
class DelieveryCrewListView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name='DeliveryCrew')
    serializer_class = UserListSerializer

    def post(self, request, *args, **kwargs):
        if request.data == {}:
            return Response({'message':'add username to body'})
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="DeliveryCrew")
            managers.user_set.add(user)
            return Response({"message": 'Added user to Delivery Crew Group'}, status.HTTP_201_CREATED)
            return Response({'message': 'add username to value field'}, status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request, *args, **kwargs):
        if request.data == {}:
            return Response({'message':'add username to body'})
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="DeliveryCrew")
            managers.user_set.remove(user)
            return Response({'message': 'Removed user from Delivery Crew Group'}, status.HTTP_200_OK) 
        return Response({'message': 'add username to value field'}, status.HTTP_400_BAD_REQUEST)

    
    
