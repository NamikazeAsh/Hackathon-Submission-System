# Generated by Django 4.0.1 on 2023-04-16 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HackathonApp', '0006_alter_submissionmodel_sublink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissionmodel',
            name='hackathonid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HackathonApp.hackathonmodel'),
        ),
    ]