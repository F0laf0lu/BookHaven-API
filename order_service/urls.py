from django.urls import path
from .views import OrderListView, AddtoCartView, CartCount, CartItemView, UpdateCartView, CreateOrderView, MakePaymentView, RetrieveOrderview, VerifyPaymentView


urlpatterns = [
    # Cart count
    path('cart_count', CartCount.as_view()), 
    path('update-cart', UpdateCartView.as_view(), name='get-cart'),
    # Add book to cart
    path('addbook', AddtoCartView.as_view(), name='additem'),  
    # Cart Item
    path('item', CartItemView.as_view(), name='cart-item'), 
    path('orders', OrderListView.as_view(), name='order'), 
    path('create-order', CreateOrderView.as_view(), name='order'), 
    path('orders/<int:pk>', RetrieveOrderview.as_view()), 
    path('make-payment/<int:order_id>', MakePaymentView.as_view()), 
    path('verify-payment/<str:reference>', VerifyPaymentView.as_view())
]
