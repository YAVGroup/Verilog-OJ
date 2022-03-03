# Generated by Django 3.2.12 on 2022-03-03 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problem', '0006_auto_20210918_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemBook',
            fields=[
                ('id', models.AutoField(help_text='ProblemBook ID', primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('sequence_id', models.IntegerField(default=0, help_text='Sequence in book page')),
                ('name', models.CharField(help_text='ProblemBook name', max_length=30)),
                ('description_short', models.TextField(blank=True)),
                ('content', models.TextField(blank=True)),
                ('owner', models.ForeignKey(default=1, help_text='创建者', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
