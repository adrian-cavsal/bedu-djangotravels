# Generated by Django 3.2.9 on 2021-12-04 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('last_name', models.CharField(blank=True, max_length=80, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('genre', models.CharField(choices=[('H', 'Hombre'), ('M', 'Mujer')], max_length=1)),
                ('key', models.CharField(blank=True, max_length=40, null=True)),
                ('type', models.CharField(blank=True, max_length=45, null=True)),
            ],
        ),
    ]
