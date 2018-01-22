import scrapy

class QuotesSpider(scrapy.Spider):
  name = "quotes"
  start_urls = ['https://www.comundi.fr/achats/formation-achat-public.html']

  def parse(self, response):
    SET_SELECTOR = '.result'
    for quote in response.css(SET_SELECTOR):
      item = {}

      NAME_SELECTOR = 'h2 ::text'
      REF_SELECTOR = 'abbr ::text'

      item['name'] = quote.css(NAME_SELECTOR).extract_first()
      item['ref'] = quote.css(REF_SELECTOR).extract_first()
      
      url = response.urljoin(quote.css('a::attr(href)').extract_first())
      yield scrapy.Request(url, callback=self.parse_link, meta={'item': item})

  def parse_link(self, response):
    item = response.meta['item']
    item['day'] = response.css('table th ::text').re_first('[0-9]+')
    item['price'] = response.css('table td ins::text').re('[0-9]+')
    item['objectif'] = response.css('#objectifs1 li::text').extract()

    yield item