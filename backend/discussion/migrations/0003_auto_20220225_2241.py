# Generated by Django 3.2.12 on 2022-02-25 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0002_auto_20220225_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
    ]
