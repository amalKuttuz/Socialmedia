from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class Posts(models.Model):
    post=models.CharField(default="Added a Photo",max_length=250)
    image=models.ImageField(upload_to="images",default="images/defaultpost.jpg",null=True,blank=True)
    created_date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    likes=models.ManyToManyField(User,related_name="likes",null=True)
    @property
    def post_comments(self):
        qs=self.comments_set.all().annotate(u_count=Count('like')).order_by('-u_count')
       
        
        return qs


    def __str__(self):
        return self.post


class Comments(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,null=True,blank=True)
    comment=models.CharField(max_length=200,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    like=models.ManyToManyField(User,related_name="like",null=True)
    created_date=models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.comment

    @property
    def likecount(self):
        return self.like.all().count()
class Profile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
      bio = models.TextField(max_length=500,default="no bio", blank=True)
      following = models.ManyToManyField(User, related_name='following', blank=True)


def __str__(self):
        return f'Profile for user {self.user.username}'
