# Generated by Django 4.1.3 on 2022-12-01 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0003_alter_payment_money"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="money",
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]