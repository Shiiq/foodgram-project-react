# Generated by Django 2.2.16 on 2022-04-06 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_auto_20220405_2244'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingredient',
            new_name='ingredients',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='tag',
            new_name='tags',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='description',
            new_name='text',
        ),
    ]
