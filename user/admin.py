from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from .models import User
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = settings.AUTH_USER_MODEL
    fieldsets = (
        ("Credentials", {'fields': ('email', 'password')}),
        ("Image", {'fields': ('image',)}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {
            'fields': ("gender",'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'email', 'first_name', 'last_name',)
    list_display_links = ("email",)
    search_fields = ('last_name', 'email',)
    ordering = ('last_name',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)


# register custom user model
admin.site.register(User, CustomUserAdmin)

from django.contrib.auth.models import Group
admin.site.unregister(Group)