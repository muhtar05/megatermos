# Generated by Django 3.0.5 on 2020-05-02 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200502_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='is_menu_footer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='page',
            name='is_menu_top',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='page',
            name='type',
            field=models.CharField(choices=[('page_link', 'Статическая страница'), ('simple_link', 'Обычная ссылка')], default='simple_link', max_length=50),
        ),
    ]