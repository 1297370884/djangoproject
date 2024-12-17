from django.contrib import admin
from .models import Category, Product, User

# Register your models here.
admin.site.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'description']    # 在admin站点中显示的列
#     search_fields = ['id', 'name']  # 在admin站点中搜索的列
#     list_filter = search_fields # 在admin站点中过滤的列


admin.site.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'description', 'category']
#     search_fields = ['id', 'name', 'category']
#     list_filter = search_fields



admin.site.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user_id', 'user_name', 'email']
#     search_fields = list_display
#     list_filter = list_display
