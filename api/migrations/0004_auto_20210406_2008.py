# Generated by Django 3.1.7 on 2021-04-06 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210406_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='put_at',
            field=models.DateField(auto_now=True),
        ),
    ]
