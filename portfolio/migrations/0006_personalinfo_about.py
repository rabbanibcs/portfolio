# Generated by Django 4.1.4 on 2022-12-22 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_alter_contact_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinfo',
            name='about',
            field=models.TextField(null=True),
        ),
    ]