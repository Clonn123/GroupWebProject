# Generated by Django 5.0.2 on 2024-02-26 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_content', '0003_users_age_users_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='gender',
            field=models.CharField(choices=[('Мужчина', 'male'), ('Женщина', 'female'), ('Другое', 'other')], default='Другое', max_length=20),
        ),
    ]
