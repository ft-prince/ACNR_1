# Generated by Django 5.0.7 on 2024-08-02 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screen_app', '0003_alter_pdffile_pdf_file_alter_videofile_video_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videofile',
            name='video_duration',
            field=models.IntegerField(default=80, help_text='Duration of video in seconds'),
        ),
    ]
