from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from .permissions import IsOwnerOrReadOnly
from posts.models import Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from .serializers import FollowSerializer

from posts.models import Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').order_by('pub_date')
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(
            post=get_object_or_404(Post, id=self.kwargs['post_id']),
            author=self.request.user,
        )

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post.comments.select_related('author')


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny, )


class FollowViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.follower.all()
