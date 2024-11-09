# Generated by Django 5.1.1 on 2024-10-18 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EduPlatform', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='city',
            field=models.CharField(default='default', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='teacherprofile',
            name='years_of_experience',
            field=models.IntegerField(default=0),
        ),
    ]