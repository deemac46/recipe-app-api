"""Test for recipe API's"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def create_reciper_user(user, **params):
    """Helper to create and return sample"""

    defaults = {
        'title': 'Sample title',
        'time_minutes': '22',
        'price': Decimal('5.25'),
        'description': 'sample desc',
        'link': 'https://example.com/recipe.pdf',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)

    return recipe


class PublicRecipeAPITests(TestCase):
    """Test unauthenticated recipe tests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Auth is require to to call API"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, 401)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated recipe tests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'RecipeUser@example.com',
            'testPass123')
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        "Test retrive list of recipes"

        create_reciper_user(user=self.user)
        create_reciper_user(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_is_limited_to_user(self):
        """Test is limited to authenticated user"""

        other_user = get_user_model().objects.create_user(
            'OtherRecipeUser@example.com',
            'testPass1233')

        create_reciper_user(user=self.user)
        create_reciper_user(user=other_user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)
