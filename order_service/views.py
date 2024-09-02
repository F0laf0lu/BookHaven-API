from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from order_service.models import Cart, CartItem, Order, Payment
from .serializers import CartItemSerializer, OrderSerializer, AddItemSerializer, UpdateCartItemSerializer, CreateOrderSerializer
from .payments import PayStack


class AddtoCartView(generics.CreateAPIView):
    serializer_class = AddItemSerializer

    def post(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            kwargs['cart_id'] = cart_id
        else:
            new_cart = Cart.objects.create()
            request.session['cart_id'] = new_cart.pk
            kwargs['cart_id'] = new_cart.pk
        return super().post(request, *args, **kwargs)   

    def create(self, request, *args, **kwargs):
        cart_id = kwargs['cart_id']
        serializer = self.get_serializer(data=request.data, context={'cart_id': cart_id})
        serializer.is_valid(raise_exception=True)
        cart = Cart.objects.get(pk=cart_id)
        self.perform_create(serializer, cart)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)   

    def perform_create(self, serializer, cart):
        serializer.save(cart=cart)


class CartCount(APIView):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if not cart_id:
            return Response({'cart_count':0})
        cart = Cart.objects.filter(pk=cart_id).first()
        if not cart:
            return Response({'cart_count': 0})

        count = cart.books.count()
        return Response({'cart_count': count})


class CartItemView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    pagination_class = None

    def get_queryset(self):
        cart_id =   self.request.session.get('cart_id', None)
        if cart_id:
            return CartItem.objects.filter(cart=cart_id).select_related('book')
        else:
            return CartItem.objects.none() 

class UpdateCartView(generics.UpdateAPIView):
    serializer_class = UpdateCartItemSerializer

    def get_cart_id(self, request):
        """Retrieve the cart ID from the session or create a new cart if not found."""
        cart_id = request.session.get('cart_id', None)
        if not cart_id:
            raise ValidationError({"cart_id": "No cart found in the session."})
        return cart_id

    def get_object(self):
        """Fetch the CartItem instance for the given cart."""
        cart_id = self.get_cart_id(self.request)
        cart = Cart.objects.get(pk=cart_id)
        book_id = self.request.data.get('book_id')
        if not book_id:
            raise ValidationError({"cart_item_id": "This field is required."})
        try:
            return CartItem.objects.get(cart=cart, book=book_id)
        except CartItem.DoesNotExist:
            raise Http404("CartItem not found")

    def update(self, request, *args, **kwargs):
        cart_id = self.get_cart_id(request)
        cart = Cart.objects.get(pk=cart_id)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'cart': cart})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# List all orders for a user
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Order.objects.filter(customer = self.request.user)
        return queryset


class CreateOrderView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer

    def get_cart_id(self, request):
        """Retrieve the cart ID from the session or create a new cart if not found."""
        cart_id = request.session.get('cart_id', None)
        if not cart_id:
            raise ValidationError({"cart_id": "No cart found in the session."})
        return cart_id
    
    def get_serializer_context(self):
        # Get the cart and user ID to pass them in the context
        cart_id = self.get_cart_id(self.request)
        cart = Cart.objects.get(pk=cart_id)
        return {
            'user_id': self.request.user.id,
            'cart': cart
        }
    
    def create(self, request, *args, **kwargs):
        cart_id = self.get_cart_id(request)
        cart = Cart.objects.get(pk=cart_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        del request.session['cart_id']
        headers = self.get_success_headers(serializer.data)
        return Response({'order_id':order.id, 'total':round(order.total_price, 2)}, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveOrderview(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class MakePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = Order.objects.get(pk=order_id)

        amount = int(order.total_price*100)
        user_email = order.customer.email

        if request.user.email != user_email:
            print("Error")

        paystack = PayStack()

        response = paystack.initiate_payment(user_email, amount)
        print(response)

        access_code = response['data']['access_code']
        reference = response['data']['reference']

        Payment.objects.create(
            order=order, amount=amount, 
            customer=order.customer, 
            reference=reference, 
            access_code=access_code
        )

        return Response({'access_code':access_code, 'ref':reference, 'amount':amount, 'email':user_email}, status=status.HTTP_200_OK)
    

class VerifyPaymentView(APIView):
    def get(self, request, **kwargs):
        reference = kwargs.get('reference')
        payment = Payment.objects.get(reference=reference)
        order = payment.order

        paystack = PayStack()
        payment_status, _ = paystack.verify_payment(reference)

        if payment_status:
            payment.verified = True
            order.status = 'completed'
        else:
            order.status = 'failed'
            payment.verified = False
            return Response({'status': 'failed', 'message': 'Payment verification failed'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        payment.save()
        order.save()
        return Response({'status':'success'}, status=status.HTTP_200_OK)
