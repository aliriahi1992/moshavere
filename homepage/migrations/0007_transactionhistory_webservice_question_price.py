# Generated by Django 4.2.16 on 2025-02-14 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0006_questionhistory_webservice_campaign_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionhistory',
            name='webservice_question_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
