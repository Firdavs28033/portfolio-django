# Generated by Django 5.0.4 on 2024-05-03 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_post_thubnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thubnail',
            field=models.ImageField(blank=True, default='/images/default.jpg', null=True, upload_to='images'),
        ),
    ]
