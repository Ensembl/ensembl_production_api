# Generated by Django 2.1.15 on 2020-02-20 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ensembl_production_db', '0005_text_field_null_update'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='masterexternaldb',
            options={'verbose_name': 'External DB'},
        ),
    ]
