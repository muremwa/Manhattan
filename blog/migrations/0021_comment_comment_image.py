# Generated by Django 2.0 on 2018-08-21 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_auto_20180729_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
