from django.db import models
from django.contrib.auth.models import User


class Goal(models.Model):
    content = models.CharField(max_length=500)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Goal'
        verbose_name_plural = 'Goals'


class Metrics(models.Model):
    name = models.CharField(max_length=250, unique=True, primary_key=True)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Metric'
        verbose_name_plural = 'Metrics'


class Question(models.Model):
    content = models.CharField(max_length=500)
    goal_id = models.ForeignKey(Goal, on_delete=models.CASCADE)
    metrics = models.ManyToManyField(Metrics, blank=True)

    def get_metrics(self):
        return "\n".join([q.name for q in self.metrics.all()])

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
