# Generated by Django 3.0.8 on 2020-12-18 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stripe_payments', '0004_customercard_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=50)),
                ('transaction_id', models.CharField(max_length=100)),
                ('price', models.CharField(max_length=50)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='stripe_payments.CustomerCard')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
