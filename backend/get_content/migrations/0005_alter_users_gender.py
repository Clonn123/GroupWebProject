# Generated by Django 5.0.2 on 2024-02-26 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_content', '0004_alter_users_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='gender',
            field=models.CharField(choices=[('Мужчина', 'Мужчина'), ('Женщина', 'Мужчина'), ('Другое', 'Мужчина')], default='Другое', max_length=20),
        ),
    ]
