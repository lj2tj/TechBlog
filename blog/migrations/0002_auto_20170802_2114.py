# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='attachment',
            field=models.FileField(upload_to=b'Articles', null=True, verbose_name=b'\xe9\x99\x84\xe4\xbb\xb6'),
        ),
    ]
