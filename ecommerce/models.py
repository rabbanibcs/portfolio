from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Category'
        verbose_name_plural = 'Categories'

    # def get_absolute_url(self):
    #     return reverse("categories", kwargs={})

    def __str__(self):
        return self.name.upper()


class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='category')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'SubCategory'
        verbose_name_plural = 'SubCategories'

    def __str__(self):
        return self.name.capitalize()

def directory_path(image, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}/{2}'.format(image.subcategory.category.name,
    image.subcategory.name,
     filename)
     
class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True,)
    # label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to=directory_path , null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name.title()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.discount_price:
            print('discount price not given')
            self.discount_price = self.price
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("single_product", kwargs={
            'slug': self.slug
        })

    def add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={
            'pk': self.id
        })

    def reduce_cart_url(self):
        return reverse('reduce_cart', kwargs={
            'pk': self.id
        })

    def remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={
            'pk': self.id
        })

    def add_to_wishlist_url(self):
        return reverse('add_to_wishlist', kwargs={
            'pk': self.id
        })

    def remove_from_wishlist_url(self):
        return reverse('remove_from_wishlist', kwargs={
            'pk': self.id
        })

    def reduce_from_cart_url(self):
        return reverse("reduce-from-cart", kwargs={
            'slug': self.slug
        })

    def discount(self):
        return self.price - self.discount_price



class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name


# Cart...
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"qty {self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        return self.get_total_discount_item_price()


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping_address = models.TextField(max_length=100, null=True)
    phone = models.CharField(max_length=11, null=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.shipping_address

    class Meta:
        verbose_name_plural = 'Addresses'


# Check out...
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey(
        'Address', related_name='address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.OneToOneField(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.email+'---'+str(self.id)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


ORDER_STATUS = (
    ('P', 'Processing'),
    ('S', 'Shipping'),
    ('D', 'Delivered'),
    ('R', 'Refunded'),
)
PAYMENT_STATUS = (
    ('C', 'CashOnDelivery'),
    ('P', 'Paid'),
)


class ManageOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.CharField(choices=ORDER_STATUS, max_length=1, default='P')
    payment = models.CharField(choices=PAYMENT_STATUS, max_length=1, default='P')

    def __str__(self):
        return self.order.user.email


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
