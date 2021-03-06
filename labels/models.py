from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name

    class Meta:
        verbose_name = 'Метки'
        verbose_name_plural = 'Метки'
        ordering = ['id']
