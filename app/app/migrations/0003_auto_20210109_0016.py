# Generated by Django 3.1.5 on 2021-01-08 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210108_2129'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='command',
            options={'ordering': ['command_group__order', 'command_group__name', 'order', 'name']},
        ),
        migrations.AddField(
            model_name='window',
            name='needs_clicking_center',
            field=models.BooleanField(default=False),
        ),
    ]
