# Generated by Django 3.0.5 on 2020-04-30 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_menu_page_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousel',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
