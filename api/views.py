from rest_framework import generics, permissions, mixins, status
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django_filters import rest_framework as filters
from rest_framework.generics import GenericAPIView
from .filters import DateRangeFilterSet
from django.db.models import Count
from .serializers import UserSerializer
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import UserActivitySerializer


class PostList(LoggingMixin, generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


class PostRetrieveDestroy(LoggingMixin, generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("This isn't Your post to delete")


class LikeCreate(LoggingMixin, generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Like.objects.filter(liker=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already liked for this post')
        serializer.save(liker=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You never liked for this post')


class Analytics(GenericAPIView):
    queryset = Like.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DateRangeFilterSet

    def get(self, request):
        all_select = self.get_queryset()
        filtered_queryset = self.filter_queryset(all_select)
        result = filtered_queryset.values('post_id', 'put_at').annotate(likes=Count('pk')).order_by('-put_at')
        sum_result = filtered_queryset.count()
        analytics = [{'Likes was made': sum_result}]
        analytics.append({result})
        return Response(analytics)


@api_view(['POST'])
def signup_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'data': serializer.data},
            status=status.HTTP_201_CREATED
        )

    return Response(
        {'data': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserActivityView(LoggingMixin, RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



