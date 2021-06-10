# Generated by Django 3.2.4 on 2021-06-10 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0002_alter_entry_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='speed',
            field=models.FloatField(db_index=True, default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entry',
            name='distance',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='duration',
            field=models.FloatField(db_index=True),
        ),
    ]
