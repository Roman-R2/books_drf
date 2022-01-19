from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from store.models import Book
from store.serializers import BookSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # DjangoFilterBackend - фильтрация в url /?field=значение
    # SearchFilter Чтоб искать по двум и более полям .../?search=фраза
    # OrderingFilter - для сортировки .../?ordering=price .../?ordering=-price
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]
    filter_fields = ['price']
    # Потому, что SearchFilter, укажем поля по которым сможем искать
    search_fields = ['name', 'author_name']
    # Потому, что OrderingFilter, укажем по каким полям можем сортировать
    ordering_fields = ['price', 'author_name']


def auth(request):
    return render(request, 'oauth.html')
