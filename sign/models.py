from django.db import models

# Create your models here.
class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=200, default="")

    class Meta:
        db_table = 'user'


