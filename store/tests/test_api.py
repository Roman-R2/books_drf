import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_username'
        )
        self.book_1 = Book.objects.create(
            name='Test book 1',
            price=1000,
            author_name='Author 1'
        )
        self.book_2 = Book.objects.create(
            name='Test book 2',
            price=2000,
            author_name='Author 2'
        )
        self.book_3 = Book.objects.create(
            name='Test book Author 1',
            price=3000,
            author_name='Author 3'
        )

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer(
            [
                self.book_1,
                self.book_2,
                self.book_3,
            ],
            many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        """Тест проверяет фильтрацию..."""
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BookSerializer(
            [
                self.book_1,
                self.book_3
            ],
            many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_sorting(self):
        """Тест проверяет функционал сортировки."""
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': '-price'})
        serializer_data = BookSerializer(
            [
                self.book_3,
                self.book_2,
                self.book_1,
            ],
            many=True
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    # py manage.py test store.tests.test_api.BooksApiTestCase.test_create
    def test_create(self):
        # Смотрим сначала что книг в БД 3 штуки
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            "name": "Programmin in Python 3",
            "price": 150,
            "author_name": "Mark Summerfield"
        }
        json_data = json.dumps(data)
        # Логиним созданного в def setUp пользователя
        self.client.force_login(self.user)
        response = self.client.post(
            url,
            data=json_data,
            content_type='application/json'
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # Смотрим после создания доп. книги что книг в БД 4 штуки
        self.assertEqual(4, Book.objects.all().count())

    # py manage.py test store.tests.test_api.BooksApiTestCase.test_update
    def test_update(self):
        # book-detail если хотим update
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 1200,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        # Логиним созданного в def setUp пользователя
        self.client.force_login(self.user)
        response = self.client.put(
            url,
            data=json_data,
            content_type='application/json'
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # это потому, что в тестах book_1 не поменялся, а только в БД
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()
        self.assertEqual(1200, self.book_1.price)

    # py manage.py test store.tests.test_api.BooksApiTestCase.test_delete
    def test_delete(self):
        # Смотрим сначала что книг в БД 3 штуки
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book_1.id,))
        # Логиним созданного в def setUp пользователя
        self.client.force_login(self.user)
        response = self.client.delete(
            url,
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        # Смотрим, что после удаления книги, книг в БД теперь 2 штуки
        self.assertEqual(2, Book.objects.all().count())
