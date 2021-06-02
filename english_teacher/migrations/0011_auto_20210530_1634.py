# Generated by Django 3.1.7 on 2021-05-30 13:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('english_teacher', '0010_auto_20210527_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='english_teacher.videomaterial'),
        ),
        migrations.AlterField(
            model_name='modelurltext',
            name='date_url_create',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 16, 34, 42, 215571)),
        ),
        migrations.AlterField(
            model_name='studywords',
            name='rus_word',
            field=models.CharField(max_length=50),
        ),
    ]
