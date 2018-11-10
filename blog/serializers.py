from rest_framework.serializers import ModelSerializer

from .models import Post, Profile, Tag


class PostsSerializer(ModelSerializer):
     class Meta:
         model = Post
         fields = ("id", "name", "author", "lead_text", "image",)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'writer_name', 'image')


class PostSerializer(ModelSerializer):
    author = AuthorSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        exclude = ('likes',)
