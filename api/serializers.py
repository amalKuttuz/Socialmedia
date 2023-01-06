
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Posts,Comments

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=["email","username","password"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)
    post=serializers.CharField(read_only=True)
    likecount=serializers.CharField(read_only=True)
    class Meta:
        model=Comments
        fields=["id","post","comment","user","created_date","likecount"]
    
    def create(self,validated_data):
        pos=self.context.get("post")
        usr=self.context.get("user")
        return pos.comments_set.create(user=usr,**validated_data) 



class PostSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    post_comments=CommentSerializer(read_only=True,many=True)
    
    class Meta:
        model=Posts
        fields=[
            "id",
            "post",
            "image",
            "user",
            "post_comments"
        ]

