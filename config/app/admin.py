from django.contrib import admin

from .models import (User, Restaurant, Category, MenuItem, Order,  OrderItem,
                     Delivery, Payment, Review, Address)

admin.site.register(User)