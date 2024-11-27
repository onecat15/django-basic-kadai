from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)

# Register your models here.
# admin.site.register(Product)
admin.site.register(Product, ProductAdmin)