# BMW UK Scraper

Парсер для збору даних про вживані авто з usedcars.bmw.co.uk.

## Технології
* **Python 3.12**
* **Scrapy**
* **Playwright** (для рендерингу JS та обходу WAF)
* **SQLite** (база даних)

## Як запустити
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   scrapy crawl bmw