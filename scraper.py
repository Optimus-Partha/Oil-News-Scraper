import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai import JsonXPathExtractionStrategy
import json

async def extract_oil_gas_news():
    schema = {
        "name": "Oil News via XPath",
        "baseSelector": "//div[@class='moreEditorials__article']",
        "fields": [
            {
                "name": "Heading",
                "selector": ".//h2[@class='moreEditorials__article__title']",
                "type": "text"
            },
            {
                "name": "Article_Link",
                "selector": ".//h2[@class='moreEditorials__article__title']/a",
                "type": "attribute",
                "attribute": "href"
            },
            {
                "name": "Short_description",
                "selector": ".//p[@class='moreEditorials__article__excerpt']",
                "type": "text"
            }
        ]
    }

    config = CrawlerRunConfig(
        extraction_strategy=JsonXPathExtractionStrategy(schema, verbose=False)
    )

    try:
        async with AsyncWebCrawler(verbose=True) as crawler:
            result = await crawler.arun(
                url="https://oilprice.com/",
                config=config
            )

            if not result.success:
                print("Crawl failed:", result.error_message)
                return "", ""

            data = json.loads(result.extracted_content)
            print(f"Extracted {len(data)} articles")
            
            heading_short_descriptions_dicts = [
                {'Heading': item.get('Heading'), 'Short_description': item.get('Short_description')}
                for item in data
                if item.get('Heading') or item.get('Short_description')
            ]
            news = '\n'.join(repr(d) for d in heading_short_descriptions_dicts)

            links = [item.get('Article_Link') for item in data if item.get('Article_Link')]
            links_str = '\n'.join(links)

        return news, links_str
    except Exception as e:
        print(f"Error in scraper: {e}")
        import traceback
        traceback.print_exc()
        return "", ""

if __name__ == "__main__":
    news, links = asyncio.run(extract_oil_gas_news())
    print(news, links)