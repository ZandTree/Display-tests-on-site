# Generated by Django 2.0.1 on 2019-06-25 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=124)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=124)),
                ('description', models.TextField()),
                ('order', models.IntegerField(default=0)),
                ('content', models.TextField(default='')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.Group')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
    ]
