from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from post.models import Post
from django.shortcuts import render

def react_app(request):
    return render(request, 'index.html')




class PostSerializer(serializers.ModelSerializer):
        tags = serializers.StringRelatedField(many=True)

        class Meta:
            model = Post
            fields = '__all__'

class PostViewSet(viewsets.ModelViewSet):
        queryset = Post.objects.all()
        serializer_class = PostSerializer
        permission_classes = [IsAuthenticatedOrReadOnly]
