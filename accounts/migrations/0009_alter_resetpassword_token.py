# Generated by Django 5.1.6 on 2025-02-11 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_alter_resetpassword_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resetpassword",
            name="token",
            field=models.CharField(editable=False),
        ),
    ]
