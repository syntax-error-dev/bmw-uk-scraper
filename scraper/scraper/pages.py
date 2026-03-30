class BMWPage:
    SEARCH_CARD = "h3.uvl-c-advert-overview__title"
    NEXT_BUTTON = "a.uvl-c-pagination__link--next"

    TITLE = "h1.uvl-c-vehicle-identifier__title"
    MODEL = "p.uvl-c-vehicle-identifier__model"
    SPEC_TITLE = "div.uvl-c-specification-overview__title"
    SPEC_VALUE = "div.uvl-c-specification-overview__value"

    @staticmethod
    def get_spec_xpath(name):
        return f'//div[contains(@class, "uvl-c-specification-overview__title") and contains(., "{name}")]/following-sibling::div/text()'