# Generated by Django 2.0 on 2020-03-09 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('face_login', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='referralemployee',
            options={'verbose_name': 'Referral', 'verbose_name_plural': 'Referral'},
        ),
        migrations.RemoveField(
            model_name='referralemployee',
            name='user',
        ),
    ]
