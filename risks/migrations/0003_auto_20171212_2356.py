# Generated by Django 2.0 on 2017-12-12 23:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('risks', '0002_auto_20171212_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='risk',
            name='instance_of',
        ),
        migrations.AddField(
            model_name='risk',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='risk',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='riskenumfield',
            name='possible_values',
            field=models.TextField(blank=True, null=True),
        ),
    ]
