# Generated by Django 3.0.5 on 2020-04-30 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200424_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShockPriceProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Product')),
            ],
            options={
                'verbose_name': 'Успейте купить по шок-цене!',
                'verbose_name_plural': 'Успейте купить по шок-цене!',
                'ordering': ['position'],
            },
        ),
    ]
