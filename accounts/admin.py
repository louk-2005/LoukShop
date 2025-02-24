#django files
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#your file
from .models import User, ResetPassword

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('phone', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser','id')
    list_filter = ('is_active', 'is_superuser')
    search_fields = ('phone', 'email')
    ordering = ('phone',)
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = [
        (None, {'fields': ('phone','password')}),
        ('Info', {'fields': ('first_name', 'last_name','email')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser','is_staff')}),
        ('Time', {'fields': ('created_at', 'updated_at')}),
    ]
    add_fieldsets = (
        (None, {'fields': ('phone', 'email', 'password1', 'password2')}),
    )
@admin.register(ResetPassword)
class ResetPasswordAdmin(admin.ModelAdmin):
    readonly_fields = ('token',)
    list_display = ('email', 'token','created_at')







