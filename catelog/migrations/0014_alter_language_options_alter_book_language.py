# Generated by Django 5.1.6 on 2025-02-16 20:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catelog', '0013_book_language'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='language',
            options={},
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catelog.language'),
        ),
    ]
