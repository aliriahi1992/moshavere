# Generated by Django 4.2.16 on 2025-01-28 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_forget',
            field=models.BooleanField(default=False),
        ),
    ]
