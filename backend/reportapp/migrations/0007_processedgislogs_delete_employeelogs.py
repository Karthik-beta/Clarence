# Generated by Django 4.2.4 on 2023-08-12 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportapp', '0006_alter_employeelogs_first_logtime_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessedGislogs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('employeeid', models.IntegerField(blank=True, null=True)),
                ('direction', models.CharField(blank=True, max_length=50, null=True)),
                ('shortname', models.CharField(blank=True, max_length=50, null=True)),
                ('serialno', models.CharField(blank=True, max_length=50, null=True)),
                ('logdate', models.DateField(blank=True, null=True)),
                ('first_logtime', models.TimeField(blank=True, null=True)),
                ('last_logtime', models.TimeField(blank=True, null=True)),
                ('total_time', models.DurationField(null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='employeeLogs',
        ),
    ]
