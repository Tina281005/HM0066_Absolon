# Generated by Django 5.1.1 on 2025-03-02 06:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_gad7response_user_alter_gad7response_total_score_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='gad7response',
            name='user',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='gad7_responses', to=settings.AUTH_USER_MODEL),
        ),
    ]
