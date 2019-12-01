from unittest import TestCase

from pipelines import AlephPipeline


class TestPipeline(TestCase):

    def test_AlephPipeline(self):
        key = '1234'
        host = 'https://example.com'

        aleph = AlephPipeline(key, host)
