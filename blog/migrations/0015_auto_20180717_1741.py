# Generated by Django 2.0 on 2018-07-17 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20180717_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_text',
            field=models.CharField(max_length=2000),
        ),
    ]
