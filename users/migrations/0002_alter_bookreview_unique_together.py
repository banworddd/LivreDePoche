# Generated by Django 5.1.2 on 2024-10-31 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookreview',
            unique_together={('user', 'book')},
        ),
    ]