# Generated by Django 4.0.1 on 2023-04-16 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HackathonApp', '0012_alter_submissionmodel_userid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submissionmodel',
            name='userid',
        ),
    ]
