from django.contrib.auth.models import User
from django.test import TestCase

from store.logic import set_rating
from store.models import Book, UserBookRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
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

        self.book_1 = Book.objects.create(
            name='Test book 1',
            price=1000,
            author_name='Author 1',
            owner=user_1
        )

        UserBookRelation.objects.create(user=user_1, book=self.book_1,
                                        like=True, rate=5)
        UserBookRelation.objects.create(user=user_2, book=self.book_1,
                                        like=True, rate=5)
        UserBookRelation.objects.create(user=user_3, book=self.book_1,
                                        like=True, rate=4)

    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('4.67', str(self.book_1.rating))
