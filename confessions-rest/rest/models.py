from django.db import models
from django.contrib.auth.models import User
# Create your models here.


vote_choices = ((1, 'UPVOTE'), (2, 'DOWNVOTE'))


class Confession(models.Model):
    id = models.AutoField(primary_key=True)
    heading = models.CharField(max_length=500, null=False)
    text = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    
    def filter_deleted_comment(self):
        return Comment.objects.filter(
            confession=self, 
            deleted=False
        )

    def get_upvotes_count(self):
        return Vote.objects.filter(confession=self, vote_type=1).count()

    def get_downvotes_count(self):
        return Vote.objects.filter(confession=self, vote_type=-1).count()


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='votes', null=False)
    comment = models.ForeignKey(to="Comment", on_delete=models.PROTECT, related_name="comment_votes", null=True)
    confession = models.ForeignKey(to="Confession", on_delete=models.PROTECT, related_name="confession_votes", null=True)
    created = models.DateTimeField(auto_now_add=True)
    vote_type = models.IntegerField(choices=vote_choices, default=1)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        if hasattr(self, 'confession'):
            return 'Vote {} by {} on confession id {}'.format(self.vote_type, self.user.username, self.confession.id)
        elif hasattr(self, 'comment'):
            return 'Vote {} by {} on comment id {}'.format(self.vote_type, self.user.username, self.comment.id)
        else:
            raise Exception('Vote {} invalid'.format(self.id))


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comments', null=False)
    confession = models.ForeignKey(to="Confession", on_delete=models.PROTECT)
    text = models.TextField(max_length=2000, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text

    def get_upvotes_count(self):
        return Vote.objects.filter(confession=self, vote_type=1).count()

    def get_downvotes_count(self):
        return Vote.objects.filter(confession=self, vote_type=-1).count()
