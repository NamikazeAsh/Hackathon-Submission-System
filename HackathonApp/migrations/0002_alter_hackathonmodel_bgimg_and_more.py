# Generated by Django 4.0.1 on 2023-04-14 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HackathonApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hackathonmodel',
            name='bgimg',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='hackathonmodel',
            name='hkimg',
            field=models.ImageField(upload_to='images/'),
        ),
    ]