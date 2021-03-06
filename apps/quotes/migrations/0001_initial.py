# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-25 17:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_author', models.CharField(max_length=255)),
                ('content', models.TextField(max_length=5000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='quote',
            name='favorite',
            field=models.ManyToManyField(related_name='favorite', to='quotes.User'),
        ),
        migrations.AddField(
            model_name='quote',
            name='quote_submit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quote_submit', to='quotes.User'),
        ),
    ]
