# Generated by Django 4.0.1 on 2023-04-14 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HackathonApp', '0002_alter_hackathonmodel_bgimg_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hackathonmodel',
            name='enddate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='hackathonmodel',
            name='startdate',
            field=models.DateField(),
        ),
    ]
