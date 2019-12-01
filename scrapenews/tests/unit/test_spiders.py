"""
Test spiders.

Light testing to ensure that the syntax of the spiders is correct by loading
each spider class from the spider modules. Methods are not tested.
"""
from unittest import TestCase


from utils import list_spiders


class TestSpiders(TestCase):

    def test_names(self):
        spiders = list_spiders.get_spiders()

        self.assertTrue(len(spiders.keys()) > 0)
