# Generated by Django 5.1.6 on 2025-02-23 07:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_remove_productvariant_variation"),
    ]

    operations = [
        migrations.AddField(
            model_name="productvariant",
            name="variation",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Vproducts",
                to="products.variation",
            ),
        ),
    ]
