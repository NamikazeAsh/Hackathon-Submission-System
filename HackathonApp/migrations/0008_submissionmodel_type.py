# Generated by Django 4.0.1 on 2023-04-16 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HackathonApp', '0007_alter_submissionmodel_hackathonid'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissionmodel',
            name='type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
