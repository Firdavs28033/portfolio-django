# Generated by Django 5.0.4 on 2024-05-08 11:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_postcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.profile'),
        ),
    ]