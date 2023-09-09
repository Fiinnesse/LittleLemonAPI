from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category, ShoppingCart
from .serializers import MenuItemSerializer, CategorySerializer, UserListSerializer, CartSerializer, CartHelpSerializer
from .serializers import CartAddSerializer, CartRemoveSerializer
from rest_framework import generics, filters, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User, Group
from .permissions import AdminOrReadOnly
from django.core.exceptions import ValidationError





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
    
class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    
    def get_queryset(self, *args,**kwargs):
        if (self.request.user):
            cart = ShoppingCart.objects.all()
            return cart
        else:
            cart = ShoppingCart.objects.filter(user=self.request.user)
            return cart
    def post(self, request, *args, **kwargs):
        item = CartAddSerializer(data=request.data)
        item.is_valid(raise_exception=True)
        id = request.data['items']
        quantity = request.data['quantity']
        item = get_object_or_404(MenuItem, id=id)
        price = int(quantity) * item.price
        try:
            ShoppingCart.objects.create(user=request.user, quantity=quantity,
                                        unit_price = item.price, price = price,
                                        items_id =id)
        except:
            return Response({'message': 'Item currently in Cart, increase quantity.'}, status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Item added to cart!'})
    
    def delete(self, request, *args, **kwargs):
        if request.data['items']:
            item = CartRemoveSerializer(data=request.data)
            item.is_valid(raise_exception=True)
            menuitem = request.data['items']
            cart = get_object_or_404(ShoppingCart, user=request.user, items=menuitem)
            cart.delete()
            return Response({'message':'Item has been removed from cart!'})
        else:
            ShoppingCart.objects.filter(user=request.user).delete()
            return Response({'message':'All items have been removed from your cart!'})
    
        
    


        
        
    
        
    
    
    
    
    
