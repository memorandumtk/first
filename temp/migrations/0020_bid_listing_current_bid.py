# Generated by Django 4.1 on 2023-05-31 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_rename_category_category_name_remove_category_item_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_bid', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='current_bid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_currentbid', to='auctions.bid'),
        ),
    ]
