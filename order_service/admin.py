from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Payment

# Register your models here.

admin.site.register(CartItem)

class CartItemInline(admin.TabularInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline,]

admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(Cart, CartAdmin)

admin.site.register(Payment)