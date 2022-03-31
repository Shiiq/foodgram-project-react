# Generated by Django 2.2.16 on 2022-03-31 21:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingridient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Ингридиент')),
                ('measurement_unit', models.CharField(max_length=50, unique=True, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IngridientQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('ingridient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingridient', to='recipes.Ingridient')),
            ],
        ),
    ]
