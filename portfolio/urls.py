from django.urls import path
from .views import *
from portfolio.admin import portfolio_admin


urlpatterns = [

    path('', index, name='index'),
    path('admin/', portfolio_admin.urls),
    
]
