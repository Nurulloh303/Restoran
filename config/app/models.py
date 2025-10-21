from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db.models import UniqueConstraint


class User(AbstractUser):
    phone = models.CharField(max_length=13, null=True, blank=True)


    def __str__(self):
        return self.username

class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    open_time = models.TimeField(null=True)
    closed_time = models.TimeField(null=True)

    def __str__(self):
        return self.name



    
class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='res/menu', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.customer.username

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.menu_item.name

class Like(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'user'], name='unique_user_order_like')
        ]

    def __str__(self):
        return f"{self.user.username} → Order #{self.order.id}"

class Comment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.comment[:30]}"


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

    def __str__(self):
        return self.delivery_person.name

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

    def __str__(self):
        return self.payment_method


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.restaurant.name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=100, default='Home')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.label
