# Generated by Django 5.1.1 on 2024-09-29 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url', '0007_alter_handler_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='handler',
            name='discription',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]