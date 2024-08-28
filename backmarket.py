from scrapy.http import HtmlResponse
import requests
import csv

cat_urls = [
    "/en-us/l/smartphones/0744fd27-8605-465d-8691-3b6dffda5969",
    "/en-us/l/macbook-and-laptops/02661471-d1ce-4d43-88e3-4bc4b7d4c8d6",
    "/en-us/l/tablets/076e3232-bda6-424b-81a4-9a6c9c08e8ee",
    "/en-us/l/consoles/afa370e4-ee3a-426a-a783-c94c899d664a",
    "/en-us/l/watches/4ee50ebd-1eb4-4436-a797-80828ce28cc5",
    "/en-us/l/sound-music-device/91ffe3ce-47dd-4e42-9096-ccf96412f3f9"
]

with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Category', 'Brand', 'Model']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for cat_url in cat_urls:
        try:
            url1 = f'https://www.backmarket.com{cat_url}'
            print(url1)

            response1 = requests.get(url1)
            html1 = HtmlResponse(url=url1, body=response1.content, encoding='utf-8')
            try:
                brand_urls = html1.xpath('//*[@aria-labelledby="3zwblmbrk6WbRklvAbZXrJ"]//a/@href').getall()
                if not brand_urls:
                    brand_urls = html1.xpath('//*[@class="md:col-span-3 col-span-1 flex"]//@href').getall()
            except:
                pass
            
            for brand_url in brand_urls:
                page = 0
                while page < 35:
                    url2 = f'https://www.backmarket.com{brand_url}'
                    # url2 = f'https://www.backmarket.com{brand_url}?p={page}'
                    print(url2)

                    response2 = requests.get(url2)
                    res = HtmlResponse(url=url2, body=response2.content, encoding='utf-8')

                    models = res.xpath('//*[@class="body-1-bold line-clamp-2"]//text()').getall()

                    for model_name in models:
                        categories = cat_url.split('/')[-2]
                        brand = brand_url.split('/')[-2]
                        model = model_name.replace('- Unlocked', '').replace('- locked', '')
                        writer.writerow({'Category': categories, 'Brand': brand, 'Model': model})

                    page += 1

        except Exception as e:
            print(f"Error occurred: {e}")
