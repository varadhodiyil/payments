# Generated by Django 3.0.8 on 2020-12-18 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_payments', '0003_auto_20201218_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='customercard',
            name='brand',
            field=models.CharField(default='visa', max_length=250),
            preserve_default=False,
        ),
    ]
