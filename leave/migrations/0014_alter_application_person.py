# Generated by Django 3.2.9 on 2021-11-22 19:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0013_alter_application_up_next'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave.person'),
        ),
    ]
