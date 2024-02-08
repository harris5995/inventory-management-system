# Generated by Django 5.0.1 on 2024-02-07 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('operator', 'Operator'), ('viewer', 'Viewer')], max_length=100),
        ),
    ]
