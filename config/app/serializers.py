from django.template.context_processors import request
from rest_framework import serializers
from .models import (
    Restaurant, User, Category, MenuItem,
    Order, OrderItem, Delivery, Payment, Review, Address, Like, Comment
)


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
        depth = 1 


class CategorySerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = Category
        fields = '__all__'
        depth = 1


class SimpleRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'address']


class MenuItemSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

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
    # restaurant = RestaurantSerializer(read_only=True)
    orderitem_set = OrderItemSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'likes', 'dislikes', 'comment']
        depth = 1

    def get_likes(self, instance):
        return instance.likes.filter(like=True).count()

    def get_dislikes(self, instance):
        return instance.likes.filter(like=False).count()

    def get_comments(self, instance):
        return instance.comments.filter(comment=True).count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'order', 'user', 'like']
        read_only_fields = ('user',)

    def validate_order(self, value):
        request = self.context.get('request')
        if value.customer != request.user:
            raise serializers.ValidationError("Siz faqat ozingz qilgan buyrtmangizuchu like bosa olasiz")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

    def validate_order(self, value):
        request = self.context.get('request')
        if value.customer != request.user:
            raise serializers.ValidationError("Sz faqat ozingiz yozgan comentariya uchun like bosa olasz holos")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OrderForSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['delivery_person', 'address', 'status']


class DeliverySerializer(serializers.ModelSerializer):
    order = OrderForSerializer()

    class Meta:
        model = Delivery
        fields = '__all__'
        depth = 1


class OrderPaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'
        depth = 1


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
