# Generated by Django 2.0.1 on 2019-06-26 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_truefalsequestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.BooleanField(default=False)),
                ('text', models.CharField(max_length=1024)),
                ('order', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ans', to='groups.Question')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]