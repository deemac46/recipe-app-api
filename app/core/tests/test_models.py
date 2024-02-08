"""
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    """Test Models. """


    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """Test emails are normalised"""

        sameple_emails= [
            ['test1@EXAMPLE.com','test1@example.com'],
            ['TesT2@EXAMPLE.Com','TesT2@example.com'],
            ['tESt3@Example.cOM','tESt3@example.com'],
        ]

        for email, expected in sameple_emails:
            user = get_user_model().objects.create_user(email,'sample123')
            self.assertEqual(user.email,expected)

    def test_new_user_without_email_raises_error(self):
        
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')

    
    def test_create_superuser(self):

        user = get_user_model().objects.create_superuser(
            'test@example.com', 'test123'
        )


        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)