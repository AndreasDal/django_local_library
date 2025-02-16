# Generated by Django 5.1.6 on 2025-02-16 14:37

import django.db.models.deletion
import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catelog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)", max_length=200, unique=True)),
            ],
            options={
                'ordering': (['name'],),
                'constraints': [models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='language_name_case_insensitive_unique', violation_error_message='Language alreade exists (case insensitive match)')],
            },
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catelog.language'),
        ),
    ]
