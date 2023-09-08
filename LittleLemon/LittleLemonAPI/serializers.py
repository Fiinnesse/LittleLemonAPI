from .models import MenuItem, Category
from rest_framework import serializers
from django.contrib.auth.models import User, Group

class CategorySerializer(serializers.ModelSerializer):
    class Meta():
        model = Category
        fields = ['id','title']


class MenuItemSerializer(serializers.ModelSerializer):
    #category_id = serializers.IntegerField(write_only=True)
    #category = CategorySerializer(read_only=True)
    class Meta():
        model = MenuItem
        fields = ['id','title','price','inventory']
        extra_kwargs = {'price':{'min_value':1},
                        'inventory':{'min_value':0}}
        
class UserListSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['username', 'email']
        
        
