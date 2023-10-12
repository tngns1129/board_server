from rest_framework import serializers
from .models import Posts, Content, Comment
from sign.models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'username')

class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('post_id', 'content')
        read_only_fields = ()

class TitleSerializer(serializers.ModelSerializer):
    #post = ContentsSerializer(many=True, read_only=True)
    user = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Posts
        fields = ('title', 'brief_description', 'updated_date', 'user', 'id', 'comment_count')
        read_only_fields = ()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user_id).data
        return response

class PostSerializer(serializers.ModelSerializer):
    #post = ContentsSerializer(many=True, read_only=True)
    user = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Posts
        fields = ('id', 'title', 'brief_description', 'created_date', 'updated_date','comment_count', 'deleted', 'user')
        read_only_fields = ()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user_id).data
        return response

class  CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = ('content', 'updated_date', 'user', 'id')
        depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user_id).data
        return response