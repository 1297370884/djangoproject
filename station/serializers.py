from station.models import Category, Product

from rest_framework import serializers


# 序列化器类定义
class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器类"""

    class Meta:
        model = Category
        fields = '__all__'


# 序列化器类定义
class ProductSerializer(serializers.ModelSerializer):
    """商品序列化器类"""
    # 外键约束 可读可写，从category.name获取数据
     # 用于GET请求输出 category.name
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    # 用于POST/PUT请求写入 category_id
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)

    class Meta:
        model = Product
        fields = '__all__'

