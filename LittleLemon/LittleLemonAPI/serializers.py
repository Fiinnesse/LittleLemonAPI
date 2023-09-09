from .models import MenuItem, Category, ShoppingCart, Order, OrderItem
from rest_framework import serializers
from django.contrib.auth.models import User, Group

class CategorySerializer(serializers.ModelSerializer):
    class Meta():
        model = Category
        fields = ['id','title']
        def __str__(self):
            return self.title

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta():
        model = MenuItem
        fields = ['id','title','price','inventory','featured','category','category_id']
        extra_kwargs = {'price':{'min_value':1},
                        'inventory':{'min_value':0},
                        'category_id' :{'min_value': 1},
                        'category_id' :{'max_value': 5},
                        }
        
class UserListSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['username', 'email']
        
        
class CartHelpSerializer(serializers.ModelSerializer):
    class Meta():
        model = MenuItem
        fields = ['id', 'title', 'price']
        
class CartSerializer(serializers.ModelSerializer):
    items = CartHelpSerializer()
    class Meta():
        model = ShoppingCart
        fields = ['items','quantity','price']
        
class CartAddSerializer(serializers.ModelSerializer):
    class Meta():
        model = ShoppingCart
        fields = ['items', 'quantity']
        extra_kwargs = {
            'quantity': {'min_value': 1},
        }   
        
class CartRemoveSerializer(serializers.ModelSerializer):
    class Meta():
        model = ShoppingCart
        fields = ['items']
 
class OrderSerializer(serializers.ModelSerializer):
    class Meta():
        model = Order    
        fields = ['id', 'user', 'total', 'status', 'delivery_crew', 'date']
        
class SingleOrderSerializer(serializers.ModelSerializer):
    menuitem = CartHelpSerializer()
    class Meta():
        mdoel = OrderItem
        fields = ['menuitem','quantity']
        
class OrderDeliveryCrew(serializers.ModelSerializer):
    class Meta():
        model = Order
        fields = ['delivery_crew']        

    
        
        
