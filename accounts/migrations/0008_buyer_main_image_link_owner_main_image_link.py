# Generated by Django 4.2.1 on 2023-07-27 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_favoriteproperty_delete_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='main_image_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='owner',
            name='main_image_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]