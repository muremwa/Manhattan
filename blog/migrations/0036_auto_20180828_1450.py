# Generated by Django 2.0 on 2018-08-28 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0035_auto_20180828_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, help_text='use MarkDown', null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_caption',
            field=models.CharField(blank=True, help_text='Describe the image', max_length=100, null=True),
        ),
    ]
