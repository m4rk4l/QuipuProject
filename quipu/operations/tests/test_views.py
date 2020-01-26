import json

from django.test import TestCase, Client
from django.urls import reverse


class TestAdditionView(TestCase):

    def test_addition_GET():
        """"""