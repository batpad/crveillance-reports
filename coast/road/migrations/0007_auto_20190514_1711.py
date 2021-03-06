# Generated by Django 2.2.1 on 2019-05-14 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('road', '0006_auto_20190513_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoreport',
            name='point_radius',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='videoreport',
            name='point_x',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='videoreport',
            name='point_y',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
