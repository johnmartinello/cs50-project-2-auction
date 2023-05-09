# Generated by Django 4.1.2 on 2023-01-05 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_rename_currentbid_listing_starterbid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='starterBid',
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='imageURL',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=32, null=True),
        ),
    ]