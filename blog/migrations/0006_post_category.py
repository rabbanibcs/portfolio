# Generated by Django 4.1.4 on 2022-12-09 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('wordpress', 'wordpress'), ('HTML', 'html')], default='wordpress', max_length=20),
        ),
    ]