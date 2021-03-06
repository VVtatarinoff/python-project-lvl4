from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from labels.models import Label
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True,
                            verbose_name='Наименование задачи')
    description = models.TextField(verbose_name='Описание задачи')
    creation_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name='Дата создания')
    author = models.ForeignKey(User, on_delete=models.RESTRICT,
                               related_name='author', verbose_name='Автор')
    executor = models.ForeignKey(User, on_delete=models.RESTRICT, null=True,
                                 related_name='executor',
                                 verbose_name='Исполнитель')
    status = models.ForeignKey(Status, on_delete=models.RESTRICT,
                               verbose_name='Текущий статус')
    labels = models.ManyToManyField(Label, through='LabelTaskIntermediate')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tasks_detail', kwargs={'pk': self.id})

    def get_full_name(self):
        return self.name

    class Meta:
        verbose_name = 'Задачи'
        verbose_name_plural = 'Задачи'
        ordering = ['id']


class LabelTaskIntermediate(models.Model):
    label_link = models.ForeignKey(Label, on_delete=models.RESTRICT)
    task_link = models.ForeignKey(Task, on_delete=models.CASCADE)
