import scrapy

base_url = "https://quotes.toscrape.com/api/quotes?page={}"
#  Start spider $ scrapy runspider <path to spider> -o <path to save file>


class QuotesSpider(scrapy.Spider):
    name = "infinity-scrolling-quotes"
    start_urls = [base_url.format(1)]

    def parse(self, response, **kwargs):
        data = response.json()
        for item in data.get("quotes", []):
            yield {
                "text": item.get("text"),
                "author": item.get("author", {}).get("name"),
                "tags": item.get("tags"),
            }

        current_page = data["page"]
        if data["has_next"]:
            next_page_url = base_url.format(current_page + 1)
            yield scrapy.Request(next_page_url)
