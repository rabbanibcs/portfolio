from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Product,Cart


def add_to_cart_for_authenticated_user(request, pk, qty=None):
    item = get_object_or_404(Product, pk=pk)
    in_cart, created = Cart.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    # new item in cart
    if created:
        in_cart.quantity = 1
        in_cart.save()
    # item already exists in cart
    else:
        if qty:
            in_cart.quantity = qty
            in_cart.save()
        else:
            in_cart.quantity += 1
            in_cart.save()
    return item


def remove_from_cart_for_authenticated_user(request, pk):
    item = get_object_or_404(Product, pk=pk)
    item_in_cart = Cart.objects.filter(user=request.user, item=item, ordered=False)
    item_in_cart.delete()


def add_to_cart_for_anonymous_user(request, pk):
    item = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart')
    if cart:
        print('in cart')
        if str(pk) in cart.keys():
            # Session is NOT modified so save it
            request.session['cart'][str(pk)] += 1
            request.session.save()
        else:
            request.session['cart'][str(pk)] = 1
            request.session.save()
    else:
        print('no cart')
        # Session is modified.
        request.session['cart'] = {int(pk): 1}
    # print(request.session.get_expiry_date())
    return item


def create_cart_while_logged_in(request, cart):
    for item_id, qty in cart.items():
        add_to_cart_for_authenticated_user(request, int(item_id), qty)


def confirm_order(order, payment=None):
    order_items = order.items.all()
    order_items.update(ordered=True)
    for item in order_items:
        item.save()
    order.ordered = True
    order.ordered_date = timezone.now()
    # if payment:
    #     order.payment = payment
    # order.address=address
    order.save()
