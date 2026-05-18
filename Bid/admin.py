from django.contrib import admin
from .models import Bid


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('project', 'freelancer', 'price', 'status', 'delivery_days', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('project__title', 'freelancer__username')
    date_hierarchy = 'created_at'
