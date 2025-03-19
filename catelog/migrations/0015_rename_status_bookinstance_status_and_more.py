# Generated by Django 5.1.6 on 2025-03-09 18:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catelog', '0014_alter_language_options_alter_book_language'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookinstance',
            old_name='Status',
            new_name='status',
        ),
        migrations.AddField(
            model_name='bookinstance',
            name='borrower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
