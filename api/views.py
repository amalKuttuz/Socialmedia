from django.shortcuts import render

# Create your views here.
from api.serializers import UserSerializer,PostSerializer,CommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import Posts,Comments

from rest_framework import authentication,permissions
from rest_framework.decorators import action

class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class PostsView(ModelViewSet):
    serializer_class=PostSerializer
    queryset=Posts.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    # localhost:8000/question/my_questions/
    @action(methods=["GET"],detail=False)
    def my_posts(self,request,*args,**kw):
        print(kw)
        qs=request.user.post_set.all()
        serializer=PostSerializer(qs,many=True)
        
        return Response(data=serializer.data)

        # qs=Questions.objects.filter(user=request.user)
    # localhost:8000/questions/1/add_answer/

    @action(methods=["post"],detail=True)
    def add_comment(self,request,*args,**kw):
        id=kw.get("pk")
        pos=Posts.objects.get(id=id)
        usr=request.user
        serializer=CommentSerializer(data=request.data,context={"post":pos,"user":usr})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    # localhost:8000/questions/1/list_answers
    
    @action(methods=["get"],detail=True)
    def list_comment(self,request,*args,**kw):
        id=kw.get("pk")
        pos=Posts.objects.get(id=id)
        qs=pos.comments_set.all()
        serializer=CommentSerializer(qs,many=True)
        return Response(data=serializer.data)
    

class CommentsView(ModelViewSet):
    serializer_class=CommentSerializer
    queryset=Comments.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    


    # localhost:8000/answers/1/up_vote
    @action(methods=["get"],detail=True)
    def like(self,request,*args,**kw):
        com=self.get_object() #answer object
        usr=request.user
        com.like.add(usr)
        return Response(data="created")








