# Generated by Django 5.1.2 on 2025-03-15 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Opis kategorii'),
        ),
    ]
