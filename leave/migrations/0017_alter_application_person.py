# Generated by Django 3.2.9 on 2021-11-22 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0016_alter_application_up_next'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='person',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='applicant', to='leave.person'),
        ),
    ]
