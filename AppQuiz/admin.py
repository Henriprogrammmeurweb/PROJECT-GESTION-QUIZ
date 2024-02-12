from django.contrib import admin
from .import models


admin.site.register(models.QuizCategory)
admin.site.register(models.LevelQuiz)
admin.site.register(models.Quiz)
