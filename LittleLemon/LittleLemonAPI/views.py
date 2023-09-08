from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework import generics, filters, pagination, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group
import json





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
    
    
    
    
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({'message':"some secret messeage"})

@api_view(['GET','POST'])
@permission_classes([IsAdminUser])
def managers(request):
    if request.method == 'GET':
        groupUsers = json.dumps(Group.objects.all())
        return Response(groupUsers)
    if request.data == {}:
        return Response({'message':'add username to body'})
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({"message": 'Added user to Manager Group'}, status.HTTP_201_CREATED)
    return Response({'message': 'add username to value field'}, status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def deliverycrew(request):
    if request.data == {}:
        return Response({'message':'add username to body'})
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        dc = Group.objects.get(name="DeliveryCrew")
        dc.user_set.add(user)
        return Response({"message": 'Added user to Delivery Crew Group'}, status.HTTP_201_CREATED)
    return Response({'message': 'add username to value field'}, status.HTTP_400_BAD_REQUEST)
    
    
