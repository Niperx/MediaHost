from django.db import models
from django.contrib.auth import get_user_model


class Photo(models.Model):
    title = models.CharField(max_length=30)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def __str__(self):
        return f'ID: {self.pk}:  {self.title}  --  {self.created_by.username}'
