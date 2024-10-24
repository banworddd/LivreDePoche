# Generated by Django 5.1.2 on 2024-10-24 08:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        ('users', '0005_alter_readinglist_book_alter_readinglist_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentlyreadinglist',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currently_read_by_users', to='books.book'),
        ),
        migrations.AlterField(
            model_name='currentlyreadinglist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currently_reading_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='plannedreadinglist',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planned_by_users', to='books.book'),
        ),
        migrations.AlterField(
            model_name='plannedreadinglist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planned_reading_list', to=settings.AUTH_USER_MODEL),
        ),
    ]