from rest_framework import serializers
from .models import Post, Like
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_tracking.models import APIRequestLog


class PostSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'poster', 'poster_id', 'created_at', 'likes']

    def get_likes(self, post):
        return Like.objects.filter(post=post).count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'put_at']


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'token']

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance


class UserActivitySerializer(serializers.ModelSerializer):
    last_request = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'last_login', 'last_request')

    def get_last_request(self, instance):
        last_request = APIRequestLog.objects.filter(user=instance).last().requested_at.strftime('%Y-%m-%d %H:%M:%S')
        return last_request

    def get_last_login(self, username):
        last_login = User.objects.get(username=username).last_login.strftime('%Y-%m-%d %H:%M:%S')
        return last_login