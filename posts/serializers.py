from rest_framework import serializers
from .models import Like,Post,Comment
from users.serializers import UserSerializer


class CommentSerializers(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializers(many=True,read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

        def get_likes_count(self,obj):
            return obj.likes.count()
