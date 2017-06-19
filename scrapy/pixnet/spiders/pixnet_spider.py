import os
import io
import json
import logging
import scrapy
from pixnet.items import PixnetItem
from bs4 import BeautifulSoup

class PixnetSpider(scrapy.Spider):
    name = 'pixnet'
    allowed_domains = ['pixnet.net', 'pixnet.tw']
    MAX_PAGE = 9999

    def __init__(self, keyword='', start=1, limit=9999, *args, **kwargs):
        super(PixnetSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.curr_page = int(start) - 1
        self.MAX_PAGE = limit
        self.start_urls = ['https://www.pixnet.net/searcharticle?q={}&page={}'.format(keyword, start)]

    def parse(self, response):
        self.curr_page += 1

        logging.info('=== PAGE#{} ==='.format(self.curr_page))
        logging.info('GET {}'.format(response.url))

        for href in response.css('.search-title a::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_post)

        if self.curr_page < PixnetSpider.MAX_PAGE:
            next_page = response.css('a.page-next::attr(href)')

            if next_page:
                url = response.urljoin(next_page.extract_first())
                logging.info('GET {}'.format(url))
                yield scrapy.Request(url, self.parse)
            else:
                logging.info('=== End of Page ===')
        else:
            logging.info('=== MAX_PAGE reached ===')

    def parse_post(self, response):
        logging.info('GET {}'.format(response.url))

        item = PixnetItem()

        item['url'] = response.url
        item['title'] = response.css('.article-head .title a::text').extract_first()
        item['date'] = ''.join(response.css('.article-head .publish span::text').extract())
        item['author'] = response.css('.author-profile .author-profile__name::text').extract_first()
        item['author_info'] = response.css('.author-profile .author-profile__info::text').extract_first()
        item['content'] = BeautifulSoup(response.css('.article-content-inner').extract_first() or response.css('.post-content').extract_first(), 'lxml').get_text().strip()

        links_text = response.css('.article-content-inner a::text').extract()
        links_href = response.css('.article-content-inner a::attr(href)').extract()
        item['links'] = list(zip(links_text, links_href)) if len(links_text) > 0 else []

        item['image_num'] = len(response.css('.article-content-inner img::attr(src)').extract())
        item['links_num'] = len(item['links'])
        item['global_cat'] = response.xpath('//div[@class="article-footer"]/ul[@class="refer"]/li[contains(text(), "全站分類")]/a/text()').extract_first()
        item['custom_cat'] = response.xpath('//div[@class="article-footer"]/ul[@class="refer"]/li[contains(text(), "分類")]/a/text()').extract_first()

        url_splits = response.url.split('/')
        filename = '-'.join([url_splits[2].split('.')[0], url_splits[-1].split('-')[0]])
        os.makedirs(self.keyword, exist_ok=True)
        with io.open('{}/{}.json'.format(self.keyword, filename), 'w', encoding='utf8') as f:
            json.dump(item.__dict__['_values'], f, ensure_ascii=False)
