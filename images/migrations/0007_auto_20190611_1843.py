# Generated by Django 2.2.2 on 2019-06-11 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0006_videofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
