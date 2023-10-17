from django.db import models
from sign.models import Users

# Create your models here.
class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    brief_description = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id', related_name='user')
    deleted = models.SmallIntegerField(default=-1)
    comment_count = models.IntegerField(default=-1)
    class Meta:
        db_table = 'post'


class Content(models.Model):
    post_id = models.OneToOneField(Posts, related_name='post', on_delete=models.CASCADE, primary_key=True, db_column='post_id', unique=True)
    content = models.TextField(max_length=100)
    large_content = models.TextField()
    class Meta:
        db_table = 'post_content'

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Posts, related_name='post_comment', on_delete=models.CASCADE, db_column='post_id')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id', related_name='user_comment')
    content = models.TextField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deleted = models.SmallIntegerField()
    class Meta:
        db_table = 'comment'


