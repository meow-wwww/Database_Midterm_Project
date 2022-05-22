# from tkinter import models.CASCADE
from django.db import models
from datetime import datetime

# Create your models here.
class User(models.Model):
    name = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField()

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)

class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=100)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    sender_id = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    receiver_id = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)

class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    following = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    be_followed = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)