# Generated by Django 2.0.6 on 2018-07-27 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0003_thing_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_title', models.CharField(max_length=200)),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='things.Thing')),
            ],
        ),
    ]
