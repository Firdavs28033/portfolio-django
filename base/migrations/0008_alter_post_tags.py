# Generated by Django 5.0.4 on 2024-05-03 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_rename_thubnail_post_thumbnail_alter_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='base.tags'),
        ),
    ]
