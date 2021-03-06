# Generated by Django 3.0.5 on 2020-05-03 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_product_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ranking', models.PositiveSmallIntegerField(default=0)),
                ('primary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_recommendations', to='catalog.Product')),
                ('recommendation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Product', verbose_name='Recommended product')),
            ],
            options={
                'verbose_name': 'Похожие товары',
                'verbose_name_plural': 'Похожие товары',
                'ordering': ['primary', 'ranking'],
                'unique_together': {('primary', 'recommendation')},
            },
        ),
    ]
