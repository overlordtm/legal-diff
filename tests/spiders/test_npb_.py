import unittest
from betamax.fixtures.unittest import BetamaxTestCase
from scrapy.http import HtmlResponse
from betamax.decorator import use_cassette
from pisrs_scraper.spiders.npb import NpbSpider
import json

class TestNpbSpider(BetamaxTestCase):

    def setUp(self):
        super(TestNpbSpider, self).setUp()
        self.spider = NpbSpider(url='http://www.pisrs.si/Pis.web/pregledNpb?idPredpisa=ZAKO7017&idPredpisaChng=ZAKO6175')

    def test_parse(self):

        response = self.session.get(self.spider.url)

        scrapy_response = HtmlResponse(body=response.content, url=self.spider.url)

        item = self.spider.parse(scrapy_response)

        self.assertEqual(item.title, 'O SOCIALNEM PODJETNIŠTVU (ZSocP)')
        self.assertEqual(item.code, 'O SOCIALNEM PODJETNIŠTVU (ZSocP)')

        # print(item.code)
        print(item.to_json(indent=2))
        assert True