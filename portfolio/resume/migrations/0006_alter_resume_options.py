# Generated by Django 3.2.9 on 2021-11-05 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0005_auto_20211105_0743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resume',
            options={'ordering': ('resume_date',)},
        ),
    ]
