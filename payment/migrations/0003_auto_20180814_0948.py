# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_car_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='charge_id',
            field=models.CharField(max_length=999),
        ),
        migrations.AlterField(
            model_name='car',
            name='customer_id',
            field=models.CharField(max_length=999),
        ),
    ]
