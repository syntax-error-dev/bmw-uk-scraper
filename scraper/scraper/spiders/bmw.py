import scrapy
from scrapy_playwright.page import PageMethod
from ..pages import BMWPage

class BMWSpider(scrapy.Spider):
    name = "bmw"

    MAX_PAGES = 5

    def start_requests(self):
        url = "https://usedcars.bmw.co.uk/result/?payment_type=cash&size=23&source=home"
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_load_state", "networkidle"),
                    PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    PageMethod("wait_for_selector", BMWPage.SEARCH_CARD),
                ]
            }
        )

    def parse(self, response):
        car_links = response.css(f'{BMWPage.SEARCH_CARD} a::attr(href)').getall()
        self.logger.info(f"Знайдено {len(car_links)} автомобілів на сторінці")

        for link in car_links:
            yield response.follow(
                link,
                callback=self.parse_car,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "domcontentloaded"),
                        PageMethod("wait_for_selector", BMWPage.TITLE)
                    ]
                }
            )

        current_page = response.meta.get("page_number", 1)
        if current_page < self.MAX_PAGES:
            next_page = response.css(f"{BMWPage.NEXT_BUTTON}::attr(href)").get()
            if next_page:
                self.logger.info(f"Перехід на сторінку {current_page + 1}")
                yield response.follow(
                    next_page,
                    callback=self.parse,
                    meta={
                        "playwright": True,
                        "page_number": current_page + 1,
                        "playwright_page_methods": [
                            PageMethod("wait_for_load_state", "networkidle"),
                            PageMethod("wait_for_selector", BMWPage.SEARCH_CARD)
                        ]
                    }
                )

    def parse_car(self, response):
        item = {
            "name": response.css(f"{BMWPage.TITLE}::text").get("").strip(),
            "model": response.css(f"{BMWPage.MODEL}::text").get("").strip(),
            "registration": response.xpath(BMWPage.get_spec_xpath("Registration")).get("").strip(),
            "mileage": response.xpath(BMWPage.get_spec_xpath("Mileage")).get("").strip(),
            "registered": response.xpath(BMWPage.get_spec_xpath("Registered")).get("").strip(),
            "engine": response.xpath(BMWPage.get_spec_xpath("Engine")).get("").strip(),
            "fuel": response.xpath(BMWPage.get_spec_xpath("Fuel")).get("").strip(),
            "transmission": response.xpath(BMWPage.get_spec_xpath("Transmission")).get("").strip(),
            "exterior": response.xpath(BMWPage.get_spec_xpath("Exterior")).get("").strip(),
            "upholstery": response.xpath(BMWPage.get_spec_xpath("Upholstery")).get("").strip(),
        }

        if not item["registration"]:
            self.logger.warning(f"Критичні дані відсутні за посиланням: {response.url}")

        yield item