from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
# from django.db.models.deletion import CASCADE
# Create your models here.

# our custom user model instead of using django inbuilt user model we  import and used the Abstract user model
class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True,null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True,default="avatar.svg")
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host= models.ForeignKey(User,on_delete=models.SET_NULL,null=True) 
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True) 
    name = models.CharField(max_length = 200)
    description = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants',blank=True) #a user in a chat room
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # To make the latest message be the first in the chat room
    class Meta:
        ordering = ['-updated','-created'] # makes the updated messages first in the chatroom
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)  #to prevent a user from removing all the members of the group when he leaaves the group
    room = models.ForeignKey(Room,on_delete=models.CASCADE)  #to prevent a user from deleting a group when he leaaves the group
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    # To make the latest message be the first in the message recent activities
    class Meta:
        ordering = ['-updated','-created'] # makes the updated messages first in the chatroom


    def __str__(self):
        return self.body[0:50]