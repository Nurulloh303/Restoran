from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from app.models import Order, MenuItem, User

from app.serializers import OrderSerializer, MenuItemSerializer

class OrderTestCase(APITestCase):
    def test_get(self):
        user1 = User.objects.create(username='Nodir')
        user2 = User.objects.create(username='Ali')
        user3 = User.objects.create(username='Sobir')
        user4 = User.objects.create(username='Jamila')
        order1 = Order.objects.create(customer=user1, restaurant='Rayyon', status='Pending', total_price=500, created_at=datetime.now())
        order2 = Order.objects.create(customer=user2, restaurant='Malika', status='Cancelled', total_price=2360, created_at=datetime.now())
        order3 = Order.objects.create(customer=user3, restaurant='Cafe', status='Accepted', total_price=203, created_at=datetime.now())
        order4 = Order.objects.create(customer=user4, restaurant='Munisa', status='Delivered', total_price=400, created_at=datetime.now())

        url = reverse('order-detail')

        serializer = OrderSerializer([order1, order2, order3, order4], many=True)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class MenuItemTestCase(APITestCase):
    def test_get(self):
        user1 = User.objects.create(username='Ali')
        user2 = User.objects.create(username='Sobir')
        user3 = User.objects.create(username='Jamila')
        menu1 = MenuItem.objects.create(restaurant=user1, category='Breakfast', name='Palov', description='Juda mazali', price='124500')
        menu2 = MenuItem.objects.create(restaurant=user2, category='Dinner', name='Shorva', description='Juda mazali', price='654321')
        menu3 = MenuItem.objects.create(restaurant=user3, category='Lunch', name='lagmon', description='Juda mazali', price='123456')

        url = reverse('menuitem-detail')

        serializer = MenuItemSerializer([menu1, menu2, menu3], many=True)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)