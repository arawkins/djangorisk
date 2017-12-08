# Generated by Django 2.0 on 2017-12-08 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risks', '0004_auto_20171208_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riskdatetimefield',
            name='value',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='risknumberfield',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=24, null=True),
        ),
        migrations.AlterField(
            model_name='risktextfield',
            name='value',
            field=models.TextField(blank=True, null=True),
        ),
    ]
