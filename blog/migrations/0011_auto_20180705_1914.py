# Generated by Django 2.0 on 2018-07-05 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20180705_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='user_data',
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Profile'),
        ),
    ]
