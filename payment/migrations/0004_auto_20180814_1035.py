# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20180814_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='plan_id',
            field=models.CharField(default='', max_length=999),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='subscription_id',
            field=models.CharField(default='', max_length=999),
            preserve_default=False,
        ),
    ]
