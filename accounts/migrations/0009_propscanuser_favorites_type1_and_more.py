# Generated by Django 4.2.1 on 2023-07-27 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_listing', '0011_alter_propertytype1_options_and_more'),
        ('accounts', '0008_buyer_main_image_link_owner_main_image_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='propscanuser',
            name='favorites_type1',
            field=models.ManyToManyField(blank=True, related_name='favorited_by', to='property_listing.propertytype1'),
        ),
        migrations.AddField(
            model_name='propscanuser',
            name='favorites_type2',
            field=models.ManyToManyField(blank=True, related_name='favorited_by', to='property_listing.propertytype2'),
        ),
        migrations.AddField(
            model_name='propscanuser',
            name='favorites_type3',
            field=models.ManyToManyField(blank=True, related_name='favorited_by', to='property_listing.propertytype3'),
        ),
        migrations.DeleteModel(
            name='FavoriteProperty',
        ),
    ]