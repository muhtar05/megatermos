# Generated by Django 3.0.5 on 2020-05-02 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20200502_1807'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seomodulefilterurl',
            options={'ordering': ('url',), 'verbose_name_plural': 'Сгенерированные страницы'},
        ),
        migrations.AddField(
            model_name='seomodulefilterurl',
            name='parameters',
            field=models.TextField(blank=True),
        ),
    ]
