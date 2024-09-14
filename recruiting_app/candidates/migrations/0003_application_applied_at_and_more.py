# Generated by Django 5.1.1 on 2024-09-14 04:44

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0002_candidateprofile_bio_candidateprofile_skills'),
        ('hr', '0002_remove_jobposting_created_by_jobposting_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='applied_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='cover_letter',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='job_posting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_applications', to='hr.jobposting'),
        ),
        migrations.AlterField(
            model_name='application',
            name='match_score',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='candidateprofile',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='candidateprofile',
            name='skills',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
