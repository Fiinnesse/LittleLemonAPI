from django.contrib import admin
from .models import MenuItem, Category, ShoppingCart, Order, OrderItem

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(ShoppingCart)
admin.site.register(Order)