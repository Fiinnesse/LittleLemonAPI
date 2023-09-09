from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category, ShoppingCart, Order, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer, UserListSerializer, CartSerializer, CartHelpSerializer
from .serializers import CartAddSerializer, CartRemoveSerializer, OrderSerializer, OrderDeliveryCrew, SingleOrderSerializer
from rest_framework import generics, filters, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User, Group
from .permissions import AdminOrReadOnly
from django.core.exceptions import ValidationError
import math
from datetime import date





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

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self, *args, **kwargs):
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser == True:
            query = Order.objects.all()
        elif self.request.user.groups.filter(name='DeliveryCrew').exists():
            query = Order.objects.filter(delivery_crew=self.request.user)
        else:
            query = Order.objects.filter(user=self.request.user)
        return query
    
    def get_permissions(self):
        if self.request.method == 'GET' or 'POST':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def post(self, request, *args, **kwargs):
        cart = ShoppingCart.objects.filter(user=request.user)
        x=cart.values_list()
        if len(x) == 0:
            return Response({'message': 'Bad Response'}, status.HTTP_400_BAD_REQUEST)
        total = math.fsum([float(x[-1]) for x in x])
        order = Order.objects.create(user=request.user, status=False, total=total, date=date.today())
        for i in cart.values():
            items = get_object_or_404(MenuItem, id=i['items_id'])
            orderitem = Order.objects.create(order=order, items=items, quantity=i['quantity'])
            orderitem.save()
        cart.delete()
        return Response({'message':'Your order has been placed! Your order number is {}'.format(str(order.id))}, status.HTTP_201_CREATED)

class SingleOrderView(generics.ListCreateAPIView):
    serializer_class = SingleOrderSerializer()
    
    def get_permissions(self):
        order = Order.objects.get(pk=self.kwargs['pk'])
        if self.request.user == order.user and self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return[permission() for permission in permission_classes] 

    def get_queryset(self, *args, **kwargs):
            query = OrderItem.objects.filter(order_id=self.kwargs['pk'])
            return query


    def patch(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order.status = not order.status
        order.save()
        return Response({'message':'Status of order #'+ str(order.id)+' changed to '+str(order.status)}, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serialized_item = OrderDeliveryCrew(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        order_pk = self.kwargs['pk']
        crew_pk = request.data['delivery_crew'] 
        order = get_object_or_404(Order, pk=order_pk)
        crew = get_object_or_404(User, pk=crew_pk)
        order.delivery_crew = crew
        order.save()
        return Response({'message':str(crew.username)+' was assigned to order #'+str(order.id)}, status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order_number = str(order.id)
        order.delete()
        return Response({'message':'Order #{} was deleted'.format(order_number)}, status.HTTP_200_OK)  
    
        
    


        
        
    
        
    
    
    
    
    
