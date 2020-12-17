# Generated by Django 3.0.8 on 2020-12-17 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('key', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expires', models.DateTimeField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'expiring_authtoken',
            },
        ),
    ]