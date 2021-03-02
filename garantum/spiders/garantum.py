import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from garantum.items import Article


class GarantumSpider(scrapy.Spider):
    name = 'garantum'
    start_urls = ['https://www.garantum.se/Kundcenter/Nyheter/']

    def parse(self, response):
        links = response.xpath('//a[@title="Läs mer"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/span/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//span[@class="date"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="innerContent"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[2:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
