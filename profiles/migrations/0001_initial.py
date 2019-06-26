# Generated by Django 2.0.1 on 2019-06-23 21:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=24)),
                ('last_name', models.CharField(default='', max_length=56)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=utils.make_avatar_path)),
                ('level', models.CharField(choices=[('start', 'beginner'), ('medium', 'intermed'), ('high', 'senior')], default='start', max_length=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]