from urllib.parse import urljoin
import scrapy

class tradeMe(scrapy.Spider):
    name = "trademe"
    start_urls = [
        'https://www.trademe.co.nz/a/property/residential/rent/auckland/rodney/dairy-flat/search?price_min=300&price_max=550&bedrooms_min=2&bedrooms_max=6',
        'https://www.trademe.co.nz/a/property/residential/rent/search?price_min=300&price_max=550&bedrooms_min=2&bedrooms_max=6&suburb=308&suburb=2634&suburb=256&suburb=150&suburb=2635&suburb=268&suburb=261&suburb=405',
        'https://www.trademe.co.nz/a/property/residential/rent/search?price_min=300&price_max=550&bedrooms_min=2&bedrooms_max=6&suburb=130&suburb=393&suburb=125&suburb=16&suburb=122&suburb=87&suburb=138&suburb=17&suburb=102&suburb=129&suburb=90&suburb=120&suburb=99&suburb=41&suburb=85&suburb=83&suburb=40&suburb=132&suburb=42&suburb=3496&suburb=109',
        'https://www.trademe.co.nz/a/property/residential/rent/search?price_min=300&price_max=550&bedrooms_min=2&bedrooms_max=6&suburb=26&suburb=15&suburb=18&suburb=24&suburb=286&suburb=273&suburb=2&suburb=25&suburb=3488',
        'https://www.trademe.co.nz/a/property/residential/rent/search?price_min=300&price_max=550&bedrooms_min=2&bedrooms_max=6&suburb=139&suburb=2982&suburb=3005&suburb=37&suburb=55&suburb=93&suburb=154&suburb=60&suburb=50&suburb=3003&suburb=51&suburb=105&suburb=96&suburb=53&suburb=95&suburb=56&suburb=3275&suburb=92&suburb=118&suburb=404&suburb=76'
    ]

    def parse(self, response):
        for i in response.css("div.o-card"):
            if i.css('a.tm-property-search-card__link::attr(href)').get() is not None:
                link = i.css('a.tm-property-search-card__link::attr(href)').get()
            else:
                link = i.css('a.tm-property-premium-listing-card__link::attr(href)').get()
            yield {
                'Available' : i.css("tm-property-search-card-address-subtitle::text").get()[11:],
                'Price' : i.css("div.tm-property-search-card-price-attribute__price::text").get()[:-9],
                'Address' : i.css("tm-property-search-card-listing-title::text").get(),
                'Link' : response.urljoin(link)
            }
        
        next_page = response.urljoin(response.css('li.o-pagination__nav-item.o-pagination__nav-item--last a::attr(href)').get())
        if next_page is not None:
            yield response.follow(next_page,self.parse)
