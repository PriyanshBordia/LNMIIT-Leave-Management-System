# Generated by Django 3.2.9 on 2021-11-22 19:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0012_alter_application_rescheduled_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='up_next',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='up_next', to='leave.person'),
        ),
    ]
