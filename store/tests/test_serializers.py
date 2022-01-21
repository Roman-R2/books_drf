from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user_1 = User.objects.create(
            username='user_1',
            first_name='first_name_1',
            last_name='last_name_1'
        )
        user_2 = User.objects.create(
            username='user_2',
            first_name='first_name_2',
            last_name='last_name_2'
        )
        user_3 = User.objects.create(
            username='user_3',
            first_name='first_name_3',
            last_name='last_name_3'
        )

        book_1 = Book.objects.create(
            name='Test book 1',
            price=1000,
            author_name='Author 1',
            owner=user_1
        )
        book_2 = Book.objects.create(
            name='Test book 2',
            price=2000,
            author_name='Author 2'
        )

        UserBookRelation.objects.create(user=user_1, book=book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user_2, book=book_1, like=True,
                                        rate=5)
        user_book_3 = UserBookRelation.objects.create(user=user_3, book=book_1,
                                                      like=True, rate=4)
        # user_book_3.rate = 4
        # user_book_3.save()

        UserBookRelation.objects.create(user=user_1, book=book_2, like=True,
                                        rate=3)
        UserBookRelation.objects.create(user=user_2, book=book_2, like=True,
                                        rate=4)
        UserBookRelation.objects.create(user=user_3, book=book_2, like=False)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(
                userbookrelation__like=True,
                then=1
            )))
        ).order_by('id')
        data = BookSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '1000.00',
                'author_name': 'Author 1',
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'user_1',
                'readers': [
                    {
                        'first_name': 'first_name_1',
                        'last_name': 'last_name_1',
                    },
                    {
                        'first_name': 'first_name_2',
                        'last_name': 'last_name_2',
                    },
                    {
                        'first_name': 'first_name_3',
                        'last_name': 'last_name_3',
                    }
                ]
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '2000.00',
                'author_name': 'Author 2',
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': '',
                'readers': [
                    {
                        'first_name': 'first_name_1',
                        'last_name': 'last_name_1',
                    },
                    {
                        'first_name': 'first_name_2',
                        'last_name': 'last_name_2',
                    },
                    {
                        'first_name': 'first_name_3',
                        'last_name': 'last_name_3',
                    }
                ]
            }
        ]
        self.assertEqual(expected_data, data)
