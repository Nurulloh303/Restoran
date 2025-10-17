from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator



class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    open_time = models.TimeField(null=True)
    closed_time = models.TimeField(null=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone = models.CharField(max_length=13, null=True, blank=True)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE, 
        null=True, blank=True
    )

    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=150)

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=2, decimal_places=2)
    image = models.ImageField(upload_to='res/menu')
    available = models.BooleanField(default=True)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('on_the_way', 'On The Way'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ])
    total_price = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[
        ('assigned', 'Assigned'),
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered'),
    ])
    estimated_time = models.DateTimeField(null=True, blank=True)

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online'),
    ])
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=100, default='Home')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

