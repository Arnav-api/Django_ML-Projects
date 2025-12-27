from django.contrib import admin
from .models import UserProduct

@admin.register(UserProduct)
class UserProductAdmin(admin.ModelAdmin):
    list_display = (
        'seller_name',
        'category',
        'price',
        'detection_status',
        'is_demo',
        'uploaded_at'
    )
    list_filter = ('category', 'detection_status', 'is_demo')
    search_fields = ('seller_name', 'category')
