# Generated by Django 2.0.6 on 2018-08-08 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0006_auto_20180804_0657'),
    ]

    operations = [
        migrations.CreateModel(
            name='Addresses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
    ]