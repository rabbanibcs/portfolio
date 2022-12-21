from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .utils import *
from django.http import HttpResponseRedirect
from django.urls import resolve
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# # Create your views here.
from django.views.generic import (ListView,
                                    DetailView,
                                    CreateView,
                                    UpdateView,
                                    DeleteView,
                                  )

class ProductsListView(ListView):
    model = Product
    template_name = 'ecommerce/products.html' 
    context_object_name = 'items'  
    ordering = ['-created_at']
    paginate_by=6

    
class NewestProductsListView(ListView):
    model = Product
    template_name = 'ecommerce/products.html' 
    context_object_name = 'items'  
    ordering = ['-created_at']
    paginate_by=6

class LowPriceProductsListView(ListView):
    model = Product
    template_name = 'ecommerce/products.html' 
    context_object_name = 'items'  
    ordering = ['price']
    paginate_by=6
   
class HighPriceProductsListView(ListView):
    model = Product
    template_name = 'ecommerce/products.html' 
    context_object_name = 'items'  
    ordering = ['-price']
    paginate_by=6
   





def product_view(request, slug):
    product = Product.objects.get(slug=slug)
    like_products = Product.objects.filter(subcategory=product.subcategory).exclude(pk=product.id)
    try:
        wished = Wishlist.objects.get(user=request.user, item=product)
    except:
        wished = None
    try:
        in_cart = Cart.objects.get(user=request.user, item=product, ordered=False)
    except:
        in_cart = None
    return render(
        request,
        'ecommerce/single-product.html',
        {'product': product, 'like_products': like_products, 'wished': wished, 'in_cart': in_cart}
    )



# Remove an item to favorite.
@login_required
def remove_from_wishlist(request, pk):
    item = Product.objects.get(pk=pk)
    wished_item, created = Wishlist.objects.get_or_create(item=item, user=request.user)
    wished_item.delete()
    messages.info(request, "Item has been removed.")

    # keep user on the same page
    next = request.META.get('HTTP_REFERER', None) or '/'
    # print(next, 'previous path')
    response = HttpResponseRedirect(next)
    return response


# Add an item to favorite.
@login_required
def add_to_wishlist(request, pk):
    item = Product.objects.get(pk=pk)
    wished_item, created = Wishlist.objects.get_or_create(item=item, user=request.user)
    messages.info(request, "Item was added to your wishlist.")
    return redirect('single_product', slug=item.slug)


# reduce item quantity by one
def reduce_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        item_in_cart = Cart.objects.get(user=request.user, item=item, ordered=False)
        if item_in_cart.quantity > 1:
            item_in_cart.quantity -= 1
            item_in_cart.save()
        else:
            remove_from_cart_for_authenticated_user(request, pk)
    else:
        cart = request.session.get('cart')
        if request.session['cart'][str(pk)] > 1:
            # Session is NOT modified so save it
            request.session['cart'][str(pk)] -= 1
            request.session.save()
        else:
            request.session['cart'].pop(str(pk))
            request.session.save()
    return redirect("cart")



# remove item from Cart.
def remove_from_cart(request, pk):
    if request.user.is_authenticated:
        print('remove_from_cart')
        remove_from_cart_for_authenticated_user(request, pk)
        return redirect("cart")
    else:
        request.session['cart'].pop(str(pk))
        request.session.save()
        return redirect("cart")


# Add a item to Cart.
def add_to_cart(request, pk):
    print('ad to cart-----------', request.method)

    if request.user.is_authenticated:
        item = add_to_cart_for_authenticated_user(request, pk)
        try:
            wish_item = Wishlist.objects.get(item=item, user=request.user)
            wish_item.delete()
        except:
            pass
        return redirect("cart")

    else:
        item = add_to_cart_for_anonymous_user(request, pk)
        # del request.session['cart']
        return redirect("cart")



def check_out(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            shipping_default = form.cleaned_data['shipping_default']
            messages.success(request, 'Order has been placed.')
            if shipping_default == 'N':
                # find past default address
                addresses = Address.objects.filter(user=request.user, default=True)
                addresses.update(default=False)
                for address in addresses:
                    address.save()
                # set new address as default
                shipping_address = form.cleaned_data.get('shipping_address')
                phone = form.cleaned_data.get('phone')
                address = Address(
                    user=request.user,
                    shipping_address=shipping_address,
                    phone=phone,
                )
                address.default = True
                address.save()
                print(address)

            else:
                address = Address.objects.filter(user=request.user, default=True).first()
                print(address)

            cart_products=Cart.objects.filter(user=request.user,ordered=False)
            for product in cart_products:
                product.ordered=True
                product.save()
            print(cart,"cart")


            order,created=Order.objects.get_or_create(user=request.user,ordered=False)
            order.items.set(cart_products)
            order.save()
            # confirm_order(order)
            print(order,'order')

            return redirect("cart")

            # return render(request, 'ecommerce/checkout.html', {'form': form, 'address': address})

    else:
        address = Address.objects.filter(user=request.user, default=True).first()
        form = CheckoutForm()
        return render(request, 'ecommerce/checkout.html', {'form': form, 'address': address})
    return render(request, 'ecommerce/checkout.html')



# show all items in Cart.
def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, ordered=False)
        cart_total = cart.count()
        # print('cart', cart_total)
        total_price = 0
        for item in cart:
            total_price += item.get_final_price()

        context = {
            'cart_total': cart_total,
            'cart': cart,
            'total_price': total_price
        }
        return render(request, 'ecommerce/cart.html', context)
    else:
        cart = request.session.get('cart', {})
        dict = {}
        for item_key, qty in cart.items():
            dict[Product.objects.get(pk=int(item_key))] = qty
        context = {
            'cart_total': len(cart),
            'cart': dict
        }
        return render(request, 'ecommerce/_cart.html', context)


# show all favorite items
@login_required(login_url='/shop/signin/')
def favorite(request):
    print('wishlist-----------', request.method)
    liked = Wishlist.objects.filter(user=request.user)
    print('wish_list')
    if liked:
        for item in liked:
            print(item.item.name)
            context = {
                'objects': liked,
            }
    else:
        context = {
                'objects': {},
            }


    # print(request.path,' present path')
    # next = request.META.get('HTTP_REFERER', None)
    # print(next, 'previous path')
    # print(request.path)
    # match = resolve(next)
    # print(match)
    
    
    return render(request, 'ecommerce/wishlist.html', context)



def index(request):
    
    return redirect('products')

def about(request):
    return render(request, 'ecommerce/about.html')


def contact(request):
    return render(request, 'ecommerce/contact.html')

def sign_in(request):
    print(request.session.get('cart'), '---cart')
    cart = request.session.get('cart')
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=email, password=password)
            print('valid user')
            login(request, user)
            if cart:
                create_cart_while_logged_in(request, cart)
            return redirect('products')
        
        except:
            return redirect('signin_shop')
        
    else:
        form = AuthenticationForm()
        return render(request, 'ecommerce/signin.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('signin_shop')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. Now login..')
            return redirect('products')
    else:
        form = SignUpForm()
    return render(request, 'ecommerce/signup.html', {'form': form})

