# Generated by Django 4.1.2 on 2023-01-05 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_bid_bidder_bid_whichlisting'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='currentBid',
            new_name='starterBid',
        ),
    ]
