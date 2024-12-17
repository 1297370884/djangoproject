from django.db import models

from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='分类名称', verbose_name='分类名称')
    description = models.TextField(help_text='分类描述', verbose_name='分类描述')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     help_text='创建人',
    #     verbose_name='创建人',
    #     default=1
    # )
    is_deleted = models.BooleanField(default=False,verbose_name='是否删除')  # 逻辑删除

    class Meta:
        db_table = 'category'  # 指定表名
        verbose_name = '分类'  # 在admin站点中显示的名称
        verbose_name_plural = '分类'  # 在admin站点中显示的复数名称

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='商品名称', verbose_name='商品名称')
    description = models.TextField(help_text='商品描述', verbose_name='商品描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类ID', default=1)  # 外键约束
    # created_by = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     help_text='创建人',
    #     verbose_name='创建人',
    #     default=1
    # )
    is_deleted = models.BooleanField(default=False,verbose_name='是否删除')
    

    class Meta:
        db_table = 'product'  # 指定表名
        verbose_name = '商品'  # 在admin站点中显示的名称
        verbose_name_plural = '商品'  # 在admin站点中显示的复数名称

    def __str__(self):
        return self.name



class User(models.Model):
    user_id = models.CharField(max_length=100,primary_key=True,verbose_name='用户ID')
    user_name = models.CharField(max_length=100,verbose_name='用户名', null=False)
    email = models.EmailField(verbose_name='邮箱', null=False, unique=True)
    phonenumber = models.CharField(max_length=11,verbose_name='手机号', null=False, unique=True)
    password = models.CharField(max_length=100,verbose_name='密码', null=False)
    location = models.CharField(max_length=100,verbose_name='地址')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        db_table = 'user'  # 指定表名
        verbose_name = '用户'  # 在admin站点中显示的名称
        verbose_name_plural = '用户'  # 在admin站点中显示的复数名称

    def __str__(self):
        return self.user_name


