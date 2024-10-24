# Generated by Django 5.1.2 on 2024-10-24 12:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        ('users', '0008_remove_plannedreadinglist_book_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookreview',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='readinglist',
            name='status',
        ),
        migrations.CreateModel(
            name='CurrentlyReadingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currently_read_by_users', to='books.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currently_reading_list', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlannedReadingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planned_by_users', to='books.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planned_reading_list', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
