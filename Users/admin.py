from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, FreelancerProfile


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'created_at')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Profile', {'fields': ('role', 'bio', 'avatar')}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('Role', {'fields': ('email', 'role')}),
    )


@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'major', 'hourly_rate', 'experience_years')
    search_fields = ('user__username', 'major', 'skills')
    list_filter = ('experience_years',)
