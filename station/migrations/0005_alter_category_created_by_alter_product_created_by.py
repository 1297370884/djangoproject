# Generated by Django 4.2.17 on 2024-12-15 20:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("station", "0004_alter_category_created_by_alter_product_created_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="created_by",
            field=models.ForeignKey(
                help_text="创建人",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="创建人",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="created_by",
            field=models.ForeignKey(
                help_text="创建人",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="创建人",
            ),
        ),
    ]
