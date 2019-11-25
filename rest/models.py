from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Confession(models.Model):
    id = models.AutoField(primary_key=True)
    heading = models.CharField(max_length=500, null=False)
    text = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    
    def filter_deleted_comment(self):
        return Comment.objects.filter(confession=self, deleted=False)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comments')
    confession = models.ForeignKey(to=Confession, on_delete=models.PROTECT)
    text = models.TextField(max_length=2000, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.text
