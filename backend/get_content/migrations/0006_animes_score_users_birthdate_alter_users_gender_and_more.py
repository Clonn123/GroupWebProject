# Generated by Django 5.0.2 on 2024-02-28 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_content', '0005_users_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='animes',
            name='score',
            field=models.FloatField(default=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='birthdate',
            field=models.DateField(default='2022-03-15'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users',
            name='gender',
            field=models.CharField(choices=[('Мужской', 'Мужской'), ('Женский', 'Женский'), ('Другой', 'Другой')], default='Другое', max_length=20),
        ),
        migrations.AlterModelTable(
            name='userprofile',
            table='user_profile',
        ),
    ]
