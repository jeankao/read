from django.contrib import admin
from teacher.models import FClass, FWork, SpeculationWork, SpeculationClass, ExamQuestion, CourseExercise

admin.site.register(FClass)

admin.site.register(FWork)

admin.site.register(SpeculationWork)

admin.site.register(SpeculationClass)

admin.site.register(ExamQuestion)

admin.site.register(CourseExercise)