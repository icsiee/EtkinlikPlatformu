# Generated by Django 5.1.3 on 2024-11-29 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_event_category_alter_event_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]