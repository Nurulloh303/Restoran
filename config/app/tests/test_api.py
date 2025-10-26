import json
from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from app.models import Order, MenuItem, User, Restaurant, Category

from app.serializers import OrderSerializer, MenuItemSerializer

class OrderTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='Toxir', password='123456')

        user1 = User.objects.create(username='Nodir')
        user2 = User.objects.create(username='Ali')
        user3 = User.objects.create(username='Sobir')
        user4 = User.objects.create(username='Jamila')
        self.order1 = Order.objects.create(customer=user1, restaurant='Rayyon', status='Pending', total_price=500, created_at=datetime.now())
        self.order2 = Order.objects.create(customer=user2, restaurant='Malika', status='Cancelled', total_price=2360, created_at=datetime.now())
        self.order3 = Order.objects.create(customer=user3, restaurant='Cafe', status='Accepted', total_price=203, created_at=datetime.now())
        self.order4 = Order.objects.create(customer=user4, restaurant='Munisa', status='Delivered', total_price=400, created_at=datetime.now())

    def test_get(self):
        url = reverse('order-detail')

        serializer = OrderSerializer([self.order1, self.order2, self.order3, self.order4], many=True)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class MenuItemTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='Ali', password='1234')
        self.user2 = User.objects.create_user(username='Sobir', password='1234')
        self.user3 = User.objects.create_user(username='Jamila', password='1234')
        self.user4 = User.objects.create_user(username='Malika', password='1234')


        self.token_url = reverse('login')
        response = self.client.post(self.token_url, data={'username': 'Ali', 'password': '1234'})
        token = response.data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        self.rest1 = Restaurant.objects.create(user=self.user1, name='Ali’s Cafe')
        self.rest2 = Restaurant.objects.create(user=self.user2, name='Sobir’s Diner')
        self.rest3 = Restaurant.objects.create(user=self.user3, name='Jamila’s Kitchen')
        self.rest4 = Restaurant.objects.create(user=self.user4, name='Malika’s kitchen')


        self.cat1 = Category.objects.create(name='Breakfast')
        self.cat2 = Category.objects.create(name='Dinner')
        self.cat3 = Category.objects.create(name='Lunch')

        self.menu1 = MenuItem.objects.create(restaurant=self.rest1, category=self.cat1, name='Palov zor',
                                             description='Juda mazali', price='124500')
        self.menu2 = MenuItem.objects.create(restaurant=self.rest2, category=self.cat2, name='Shorva',
                                             description='Juda mazali', price='123456')
        self.menu3 = MenuItem.objects.create(restaurant=self.rest3, category=self.cat3, name='Lagmon zor',
                                             description='Juda mazali', price='123456')

    def test_get(self):
        url = reverse('menuitem-list')

        serializer = MenuItemSerializer([self.menu1, self.menu2, self.menu3], many=True)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_get_filter(self):
        url = reverse('menuitem-list')
        serializer = MenuItemSerializer([self.menu1, self.menu2], many=True)

        response = self.client.get(url, data={'price': '123456'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_get_search(self):
        url = reverse('menuitem-list')


        serializer = MenuItemSerializer([self.menu1, self.menu2], many=True)

        response = self.client.get(url, data={'search': 'zor'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_order(self):

        url = reverse('menuitem-list')

        serializer = MenuItemSerializer([self.menu2, self.menu3], many=True)
        response = self.client.get(url, data={'ordering': 'price'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_create(self):

        url = reverse('menuitem-list')

        data = {
            'restaurant': self.rest4.id,
            'category': self.cat1.id,
            'name': 'Mostava',
            'description': 'Juda mazali',
            'price': '123456',
        }

        json_data = json.dumps(data)

        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(4, MenuItem.objects.all().count())

    def test_update(self):
        url = reverse('menuitem-detail', args=[self.menu1.id])

        data = {
            'restaurant': self.menu1.restaurant.id,
            'category': self.menu1.category.id,
            'name': self.menu1.name,
            'description': 'Juda zor mazali',
            'price': self.menu1.price,
        }

        json_data = json.dumps(data)

        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu1.refresh_from_db()
        self.assertEqual(response.data['description'], self.menu1.description)



    def test_update_partial(self):
        url = reverse('menuitem-detail', args=[self.menu1.id])

        data = {
            'description': 'Juda zor mazali'
        }

        json_data = json.dumps(data)

        response = self.client.patch(url, data=json_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu1.refresh_from_db()
        self.assertEqual(response.data['description'], self.menu1.description)

    def test_delete(self):
        url = reverse('menuitem-detail', args=[self.menu1.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MenuItem.objects.filter(id=self.menu1.id).count(), 0)
