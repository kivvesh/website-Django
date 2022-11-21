from django.db import models
from django.urls import reverse

class Pres(models.Model):
    title = models.CharField(max_length=200,verbose_name='Наименование')
    content = models.TextField(blank=True,verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата публикации')
    update_at = models.DateTimeField(auto_now=True,verbose_name='Дата изменения')
    document = models.FileField(upload_to='documents/%Y/%m/%d/',verbose_name='Документ',blank = True)
    is_published = models.BooleanField(default=False, verbose_name='Отображается?')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория', related_name= 'get_pres')
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('view_pres',kwargs={'pk':self.pk})

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Презентация'
        verbose_name_plural = 'Презентации'
        ordering = ['-created_at']
class Category(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name='Категории')

    def get_absolute_url(self):
        return reverse('category',kwargs={'category_id':self.pk})

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']
