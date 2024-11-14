# Generated by Django 5.1.1 on 2024-11-14 02:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EduPlatform', '0004_alter_classes_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('accepted', 'Aceptada'), ('rejected', 'Rechazada')], default='pending', max_length=10)),
                ('requested_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EduPlatform.classes')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EduPlatform.studentprofile')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EduPlatform.teacherprofile')),
            ],
        ),
    ]