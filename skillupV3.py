import scrapy

class QuotesSpider(scrapy.Spider):
  name = "quotes"
  start_urls = ['https://www.comundi.fr/']

  def parse(self, response):
    THE_SELECTOR = '.menu-2 .list-unstyled .menu-btn'
    for quote in response.css(THE_SELECTOR):
      item = {}
      FORM_SELECTOR = 'a ::text'
      item['Formation'] = quote.css(FORM_SELECTOR).extract_first() 
      url = response.urljoin(quote.css('a::attr(href)').extract_first())
      yield scrapy.Request(url, callback=self.parse_second, meta={'item': item})

  def parse_second(self, response):
    item = response.meta['item']
    FORMSEC_SELECTOR = '.col-sm-6 .h5 ::text'
    URL_SELECTOR = '.col-sm-6 a ::attr(href)'
    item['Sous-Formation'] = response.css(FORMSEC_SELECTOR).extract()
    links = response.css(URL_SELECTOR).extract()
    
    for link in links:
      url = response.urljoin(link)
      yield scrapy.Request(url, callback=self.parse_third, meta={'item': item})

  def parse_third(self, response):
    item = response.meta['item']
    for path in response.css('.result a::attr(href)').extract():
      url = response.urljoin(path)
      yield scrapy.Request(url, callback=self.parse_link, meta={'item': item})

  def parse_link(self, response):

    item = response.meta['item']
    NAME_SELECTOR = 'h1 ::text'
    REF_SELECTOR = '.ref.hidden-xs ::text'
    DAY_SELECTOR = 'table th ::text'
    PRICE_SELECTOR = 'table td ins::text'
    item['name'] = response.css(NAME_SELECTOR).extract()
    item['ref'] = response.css(REF_SELECTOR).extract()
    item['day'] = response.css(DAY_SELECTOR).re_first('[0-9]+')
    item['price'] = response.css(PRICE_SELECTOR).re('[0-9]+')
    item['url'] = response.url

    #int(item['day']) * 7

    yield item