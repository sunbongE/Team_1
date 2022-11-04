# Generated by Django 3.2.13 on 2022-11-04 06:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_alter_review_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='tag',
            field=models.CharField(choices=[('midnight_snack', '야메추'), ('dinner', '저메추'), ('lunch', '점메추'), ('morning', '아메추')], max_length=32, verbose_name='태그명'),
        ),
        migrations.AlterField(
            model_name='review',
            name='phoneNumber',
            field=models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(regex='([0-9]{2,4})-?([0-9]{3,4})-?([0-9]{4})')]),
        ),
    ]
