# Generated by Django 5.0.1 on 2024-02-07 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_alter_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('manager', 'manager'), ('operator', 'operator')], max_length=100),
        ),
    ]
