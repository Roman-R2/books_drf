from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.models import Book, UserBookRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BookSerializer, UserBooksRelationSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # DjangoFilterBackend - фильтрация в url /?field=значение
    # SearchFilter Чтоб искать по двум и более полям .../?search=фраза
    # OrderingFilter - для сортировки .../?ordering=price .../?ordering=-price
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # IsAuthenticated, IsAuthenticatedOrReadOnly - из DRF
    # IsOwnerOrReadOnly - свое разрешение
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_fields = ['price']
    # Потому, что SearchFilter, укажем поля по которым сможем искать
    search_fields = ['name', 'author_name']
    # Потому, что OrderingFilter, укажем по каким полям можем сортировать
    ordering_fields = ['price', 'author_name']

    # Чтобы записать поле модели owner при создании новой книги
    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBooksRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBooksRelationSerializer
    # Для того, чтобы не передавать id связи, а передавать id книги
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(
            user=self.request.user,
            book_id=self.kwargs['book']  # Это book в lookup_field
        )
        return obj


def auth(request):
    return render(request, 'oauth.html')
