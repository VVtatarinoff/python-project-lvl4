from django.db import models
from django.contrib.auth.models import User


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True,
                            verbose_name='Наименование задачи')
    description = models.TextField(verbose_name='Описание задачи')
    creation_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name='Дата создания')
    author = models.ForeignKey(User, on_delete=models.RESTRICT,
                               related_name='author', verbose_name='Автор')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, null=True,
                                 related_name='executor',
                                 verbose_name='Исполнитель')
    status = models.ForeignKey(Status, on_delete=models.RESTRICT,
                               verbose_name='Текущий статус')
    labels = models.ManyToManyField(Label)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задачи'
        verbose_name_plural = 'Задачи'
        ordering = ['executor_id']