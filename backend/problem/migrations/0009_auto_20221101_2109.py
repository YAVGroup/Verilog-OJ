# Generated by Django 3.2.12 on 2022-11-01 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0001_initial'),
        ('problem', '0008_auto_20221101_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='template_code_file',
        ),
        migrations.AlterField(
            model_name='problem',
            name='template_code_files',
            field=models.ManyToManyField(blank=True, help_text='模板代码文件', related_name='template_codes', to='file.File'),
        ),
    ]
