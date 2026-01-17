from django.contrib import admin
from .models import *
from django.utils.html import format_html  # custom form

# Register your models here.

class CategoryTypeAdmin(admin.ModelAdmin):
    model = CategoryType
    list_display = ['type_code', 'type_name', 'description', 'created_at']

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['code', 'category_type', 'category_name', 'description', 'created_at']


class DefaultAccountSetUpAdmin(admin.ModelAdmin):
    model = DefaultAccountSetUp
    list_display = ['code', 'category_type', 'category_name', 'account_type', 'account_category', 'glline', 'created_at']

admin.site.register(CategoryType, CategoryTypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(DefaultAccountSetUp, DefaultAccountSetUpAdmin)