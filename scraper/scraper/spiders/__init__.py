import scrapy
from scrapy_playwright.page import PageMethod


class BMWSpider(scrapy.Spider):
    name = "bmw"

    def start_requests(self):
        base_url = "https://usedcars.bmw.co.uk/result/?payment_type=cash&size=23&source=home&page={}"

        for page in range(1, 6):
            url = base_url.format(page)
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "h3.uvl-c-advert-overview__title")
                    ]
                }
            )

    def parse(self, response):
        car_links = response.css('h3.uvl-c-advert-overview__title a::attr(href)').getall()

        for link in car_links:
            yield response.follow(
                link,
                callback=self.parse_car,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "h1.uvl-c-vehicle-identifier__title")
                    ]
                }
            )

    def parse_car(self, response):
        def get_spec(spec_name):
            xpath_query = f'//div[contains(@class, "uvl-c-specification-overview__title") and contains(., "{spec_name}")]/following-sibling::div[contains(@class, "uvl-c-specification-overview__value")]/text()'
            value = response.xpath(xpath_query).get()
            return value.strip() if value else None

        item = {
            "model": response.css('p.uvl-c-vehicle-identifier__model::text').get(),
            "name": response.css('h1.uvl-c-vehicle-identifier__title::text').get(),
            "mileage": get_spec("Mileage"),
            "registered": get_spec("Registered"),
            "engine": get_spec("Engine"),
            "range": get_spec("Range"),
            "exterior": get_spec("Exterior"),
            "fuel": get_spec("Fuel"),
            "transmission": get_spec("Transmission"),
            "registration": get_spec("Registration"),
            "upholstery": get_spec("Upholstery"),
        }
        yield item