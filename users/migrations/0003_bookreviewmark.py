# Generated by Django 5.1.2 on 2024-11-27 09:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_bookreview_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookReviewMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.CharField(choices=[('like', 'Like'), ('dislike', 'Dislike')], max_length=7)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.bookreview')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('review', 'user')},
            },
        ),
    ]
