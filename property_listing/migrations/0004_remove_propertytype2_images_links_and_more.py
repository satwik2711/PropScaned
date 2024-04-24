# Generated by Django 4.2.1 on 2023-06-18 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_listing', '0003_alter_propertytype3_possession_expected_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertytype2',
            name='images_links',
        ),
        migrations.AddField(
            model_name='propertytype2',
            name='images_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='propertytype1',
            name='images_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='propertytype3',
            name='images_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
