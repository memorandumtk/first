# Generated by Django 4.1 on 2023-06-01 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_remove_listing_current_bid_listing_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
