import scrapy
from pisrs_scraper.items import LawItem, ChapterItem, ArticleItem, LawKind, ParagraphItem

class NpbSpider(scrapy.Spider):
    name = 'npb'
    allowed_domains = ['pisrs.si']

    def __init__(self, url=None, *args, **kwargs):
        super(NpbSpider, self).__init__(*args, **kwargs)
        self.url = url

    def start_requests(self):
        yield scrapy.Request(url=self.url)

    def parse(self, response):
        preamble = []
        chapters = []
        articles = []
        paragraphs = []
        chapter_title = None
        article_title = None
        title = None
        code = None


        for section in response.xpath('//div[@class="WordSection1"]/p'):
            section_cls = section.xpath('@class').get()
            if section_cls == 'Naslovpredpisa':
                title = section.xpath('.//text()').get()
                code = section.xpath('.//text()').get()
            elif section_cls == 'Poglavje':
                if chapter_title is not None:
                    chapters.append(ChapterItem(title=chapter_title, articles=articles))
                chapter_title = section.xpath('.//text()').get()
                articles = []
            elif section_cls == 'Vrstapredpisa':
                code = section.xpath('.//text()').get()
            elif section_cls == 'len': # člen
                assert chapter_title is not None
                if article_title:
                    articles.append(ArticleItem(title=article_title, children=paragraphs))
                    paragraphs = []
            elif section_cls in ['lennaslov', 'lennovele']: # naslov člena
                assert chapter_title is not None
                article_title = section.xpath('.//text()').get()
            elif section_cls in ['Odstavek', 'Alineazaodstavkom', 'tevilnatoka', 'rkovnatokazaodstavkomA3', 'Alinejazarkovnotoko', 'Zamaknjenadolobaprvinivo']:
                if chapter_title is None:
                    preamble.append(ParagraphItem(content=section.xpath('.//text()').get()))
                else:
                    paragraphs.append(ParagraphItem(content=section.xpath('.//text()').get()))
            elif section_cls in ['Opozorilo', 'NPB', 'Oddelek', 'Prehodneinkoncnedolocbe']:
                pass
            else:
                raise ValueError(f'Unknown section class {section_cls}: {section.xpath("text()").get()}')

        chapters.append(ChapterItem(title=chapter_title, articles=articles))

        item = LawItem(title=title, kind=LawKind.LAW, url=response.url, code=code, chapters=chapters, preamble=preamble)

        return item
