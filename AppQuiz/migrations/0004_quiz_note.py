# Generated by Django 5.0.1 on 2024-02-08 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppQuiz', '0003_remove_quiz_level_quizcategory_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='note',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
    ]
