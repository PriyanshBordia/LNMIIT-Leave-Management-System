# Generated by Django 3.2.9 on 2021-11-21 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0004_rename_reschedules_date_application_rescheduled_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='department',
            field=models.CharField(choices=[('CSE', 'Computer Science and Engineering'), ('ECE', 'Electronics and Communication Engineering'), ('ME', 'Mechanical-Mechatronics Engineering'), ('HSS', 'Humanities and Social Sciences'), ('MH', 'Mathematics'), ('PH', 'Physics')], default='CSE', max_length=3),
        ),
        migrations.AlterField(
            model_name='application',
            name='rescheduled_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='office_no',
            field=models.IntegerField(default='00'),
        ),
    ]
