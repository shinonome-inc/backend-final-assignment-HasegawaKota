# Generated by Django 4.0.4 on 2022-05-23 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='yourname',
            field=models.CharField(max_length=254, null=True),
        ),
    ]
