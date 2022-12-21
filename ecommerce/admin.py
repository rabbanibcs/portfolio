from django.contrib import admin
from .models import *

# Register your models here.
class EcommerceAdmin(admin.AdminSite):
    index_title="Admin Ecommerce"
    site_header="Ecommerce administration"
ecommerce_admin=EcommerceAdmin(name="ecommerce-admin")

ecommerce_admin.register(Category)
ecommerce_admin.register(SubCategory)
ecommerce_admin.register(Product)
ecommerce_admin.register(Address)
ecommerce_admin.register(Order)
ecommerce_admin.register(ManageOrder)
ecommerce_admin.register(Payment)
ecommerce_admin.register(Cart)


# admin.site.register(Category)
# admin.site.register(SubCategory)
# admin.site.register(Product)
# admin.site.register(Address)
# admin.site.register(Order)
# admin.site.register(ManageOrder)
# admin.site.register(Payment)
# admin.site.register(Cart)
