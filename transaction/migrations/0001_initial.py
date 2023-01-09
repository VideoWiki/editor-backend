# Generated by Django 3.1.2 on 2022-12-07 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange_key', models.CharField(max_length=200, null=True)),
                ('dod', models.CharField(max_length=200, null=True)),
                ('dataToken', models.CharField(max_length=200, null=True)),
                ('paid', models.BooleanField(default=True, null=True)),
                ('price', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
