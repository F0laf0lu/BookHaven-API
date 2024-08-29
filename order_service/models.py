from typing import Iterable
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from book_service.models import Book
# Create your models here.

user = get_user_model()

class Cart(models.Model):
    cart_id  = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Cart {self.pk}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='books', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = [['cart','book']]

    def __str__(self) -> str:
        return f"{self.quantity} of {self.book.title}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled')
    ]
    customer = models.ForeignKey(user, on_delete=models.PROTECT)
    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True)

    def __str__(self) -> str:
        return f'Order #{self.pk} - {self.customer.email}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.book.title} - {self.quantity} x Order #{self.order.pk}'
    

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    customer = models.ForeignKey(user, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    access_code = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.reference} - {self.amount} for Order {self.order.id}"