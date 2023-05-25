from django.contrib import admin
from .models import *


class GoalsAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'user_id')
    list_display_links = ('id', 'content')


admin.site.register(Goal, GoalsAdmin)


class MetricsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name', )


admin.site.register(Metrics, MetricsAdmin)


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'goal_id', 'get_metrics')
    list_display_links = ('id', 'content', )


admin.site.register(Question, QuestionsAdmin)