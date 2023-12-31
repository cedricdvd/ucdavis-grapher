# Generated by Django 4.2.3 on 2023-08-10 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraperapp', '0002_prerequisite_subject_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='prerequisite',
            name='course_code',
            field=models.CharField(default='placeHolder', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject', to='scraperapp.subject'),
        ),
        migrations.AlterField(
            model_name='prerequisite',
            name='course_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_id', to='scraperapp.course'),
        ),
        migrations.AlterField(
            model_name='prerequisite',
            name='subject_id',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='subject_id', to='scraperapp.subject'),
        ),
    ]
