# Generated by Django 2.0.1 on 2019-06-26 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='MulitpleChoiceQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='groups.Question')),
                ('shuffle_answers', models.BooleanField(default=False)),
            ],
            bases=('groups.question',),
        ),
    ]
