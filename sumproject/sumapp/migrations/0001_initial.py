# Generated by Django 5.0.6 on 2024-07-07 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num1', models.FloatField()),
                ('num2', models.FloatField()),
                ('num3', models.FloatField()),
                ('num4', models.FloatField()),
                ('result', models.FloatField()),
            ],
        ),
    ]
