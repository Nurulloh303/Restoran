from datetime import timezone

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from app.models import Order, MenuItem

from app.serializers import OrderSerializer, MenuItemSerializer

class OrderTestCase(APITestCase):
    def test_get(self):
        order1 = Order.objects.create(customer='Nodir', restaurant='Rayyon', status='Pending', total_price=500, created_at=timezone.now())
        order2 = Order.objects.create(customer='Ali', restaurant='Malika', status='Cancelled', total_price=2360, created_at=timezone.now())
        order3 = Order.objects.create(customer='Sobir', restaurant='Cafe', status='Accepted', total_price=203, created_at=timezone.now())
        order4 = Order.objects.create(customer='Jamila', restaurant='Munisa', status='Delivered', total_price=400, created_at=timezone.now())

        url = reverse('order-detail')

        serializer = OrderSerializer([order1, order2, order3, order4], many=True)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_orders_by_status(self):
        response = self.client.get(self.url, {'status': 'Pending'})
        filtered_orders = Order.objects.filter(status='Pending')
        serializer = OrderSerializer(filtered_orders, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class MenuItemTestCase(APITestCase):
    def test_get(self):
        menu1 = MenuItem.objects.create(restaurant='Malika', category='Breakfast', name='Palov', description='Juda mazali', price='124500')
        menu2 = MenuItem.objects.create(restaurant='Munisa', category='Dinner', name='Shorva', description='Juda mazali', price='654321')
        menu3 = MenuItem.objects.create(restaurant='Toxir', category='Lunch', name='lagmon', description='Juda mazali', price='123456')

        url = reverse('menuitem-detail')

        serializer = MenuItemSerializer([menu1, menu2, menu3], many=True)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_menu_by_category(self):
        response = self.client.get(self.url, {'category': 'Breakfast'})
        filtered_menu = MenuItem.objects.filter(category='Breakfast')
        serializer = MenuItemSerializer(filtered_menu, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
