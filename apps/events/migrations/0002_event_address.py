# Generated by Django 2.1.1 on 2018-10-30 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='address',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]