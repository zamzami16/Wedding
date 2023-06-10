from django.test import TestCase
from django.contrib.auth.models import User


class UsersTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username="yusufz", email="yusuf@gmail.com", password="yusuf"
        )

    def testUsersData(self):
        self.assertEqual(self.user.username, "yusufz")
        self.assertEqual(self.user.email, "yusuf@gmail.com")
        self.assertEqual(self.user.password, "yusuf")
