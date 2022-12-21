from django.urls import path
from .views import *
from .admin import ecommerce_admin

urlpatterns = [
    path('admin/',ecommerce_admin.urls),
    path('products/', ProductsListView.as_view(), name='products'),
    path('newest/',NewestProductsListView.as_view(), name='newest_products'),
    path('high-price/',HighPriceProductsListView.as_view(), name='high_price_products'),
    path('low-price/',LowPriceProductsListView.as_view(), name='low_price_products'),
    path('single/<slug:slug>/', product_view, name='single_product'),
    path('add-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('reduce-cart/<int:pk>/', reduce_cart, name='reduce_cart'),
    path('remove-cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('add-to-wishlist/<int:pk>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:pk>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('checkout/', check_out, name='check_out'),
    path('cart/', cart, name='cart'),
    path('favorite/', favorite, name='wishlist'),       
    path('', index, name='shop-index'),
    path('about/',about, name='about'),
    path('contact/', contact, name='contact'),
    path('signin/', sign_in, name='signin_shop'),
    path('signout/', sign_out, name='signout_shop'),
    path('signup/', sign_up, name='signup_shop'),
]