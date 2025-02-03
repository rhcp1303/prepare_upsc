from django.contrib import admin
from questions.models import PYQuestions, PYQOptions, PYQExplanations

admin.site.register(PYQuestions)
admin.site.register(PYQOptions)
admin.site.register(PYQExplanations)
