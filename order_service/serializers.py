from decimal import Decimal
from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from book_service.models import Book
from django.contrib.auth import get_user_model

user = get_user_model()

class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.book.price

class OrderItemSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer()
    class Meta:
        model = OrderItem
        fields = ['book', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'items', 'total_price', 'status']

class CreateOrderSerializer(serializers.Serializer):
    def validate(self, attrs):
        user_id = self.context.get('user_id')
        if not user_id:
            raise serializers.ValidationError({'user_id': 'User ID is required.'})
        
        try:
            user.objects.get(pk=user_id)
        except user.DoesNotExist:
            raise serializers.ValidationError({'user': 'user not found'})
        
        
        return attrs

    def create(self, validated_data):
        user_id = self.context['user_id']
        cart = self.context['cart']

        customer = user.objects.get(pk=user_id)

        order = Order.objects.create(customer=customer)

        cart_items = CartItem.objects.filter(cart=cart)

        orderitems = [
            OrderItem(order=order, 
            book=item.book, quantity=item.quantity, 
            price=item.book.price) for item in cart_items]

        OrderItem.objects.bulk_create(orderitems)

        subtotal = sum(Decimal(item.quantity) * item.price for item in order.items.all())
        vat = subtotal * Decimal('0.075') 
        shipping = Decimal('5')

        order.total_price = subtotal + vat + shipping

        order.save()

        cart.delete()

        return order

class UpdateCartItemSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(required=False)

    class Meta:
        model = CartItem
        fields = ['book_id', 'quantity']

    def validate(self, attrs):
        """Ensure the quantity is a positive integer."""
        quantity = attrs.get('quantity', None)
        if quantity is not None and quantity < 0:
            raise serializers.ValidationError({"quantity": "Quantity must be a positive integer."})
        return attrs

    def update(self, instance, validated_data):
        # Access the cart passed via context
        cart = self.context.get('cart')
        
        # Retrieve the quantity from the validated data
        quantity = validated_data.get('quantity')

        # Update the quantity of the cart item
        if quantity is not None:
            if quantity > 0:
                instance.quantity = quantity
                instance.save()
            else:
                # If quantity is 0 or less, remove the item from the cart
                instance.delete()
                return instance
        return instance

class AddItemSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    total_item = serializers.SerializerMethodField()

    def get_total_item(self, obj):
        cart_id = self.context['cart_id']
        cart = Cart.objects.get(pk=cart_id)
        count = cart.books.count()
        return count

    def validate_book_id(field, value):
        try:
            book = Book.objects.get(pk=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book does not exist")
        return value

    def create(self, validated_data):
        cart_id = self.context['cart_id']
        book_id = validated_data['book_id']
        quantity = validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart=cart_id, book=book_id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)
    
        return cart_item



