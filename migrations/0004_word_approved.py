# Generated by Django 3.2.5 on 2022-01-10 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordtree', '0003_alter_language_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
