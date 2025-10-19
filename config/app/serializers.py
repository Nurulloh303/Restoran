# from rest_framework import serializers
# from .models import (
#     Restaurant, User, Category, MenuItem,
#     Order, OrderItem, Delivery, Payment, Review, Address
# )

# class RestaurantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Restaurant
#         fields = '__all__'



# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'


# class SimpleRestaurantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Restaurant
#         fields = ['name', 'description', 'address']

# class MenuItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MenuItem
#         fields = '__all__'


# class OrderSerializer(serializers.ModelSerializer):
#     restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
#     class Meta:
#         model = Order
#         fields = '__all__'
#         depth = 1


# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = '__all__'


# class DeliverySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Delivery
#         fields = '__all__'


# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = '__all__'


# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = '__all__'


# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         fields = '__all__'



from rest_framework import serializers
from .models import (
    Restaurant, User, Category, MenuItem,
    Order, OrderItem, Delivery, Payment, Review, Address
)


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
        depth = 1 


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SimpleRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'address']


class MenuItemSerializer(serializers.ModelSerializer):
    restaurant = SimpleRestaurantSerializer(read_only=True) 

    class Meta:
        model = MenuItem
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all())
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    orderitem_set = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        depth = 1 


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
