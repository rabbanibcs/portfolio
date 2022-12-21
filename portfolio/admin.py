from django.contrib import admin
from .models import *


# Register your models here.
class PortfolioAdmin(admin.AdminSite):
    site_header = 'Portfolio administration'
    index_title="Admin Portfolio"

    
portfolio_admin=PortfolioAdmin(name='portfolio-admin')
portfolio_admin.register(PersonalInfo)