# Generated by Django 3.0.5 on 2020-06-26 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_sitemapfilter'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuickLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название страницы')),
                ('url', models.CharField(max_length=1024, verbose_name='Сгенерированный url')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta title')),
                ('meta_keywords', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta keywords')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta description')),
                ('h1', models.CharField(blank=True, max_length=255, null=True, verbose_name='H1 заголовок')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quick_links', to='catalog.Category')),
            ],
        ),
    ]