import scrapy

class BookSpider(scrapy.Spider):
    name = 'bookworm'
    start_urls = ['https://santrapub.com/collections/all']

    def parse(self, response):
        
        # Fetch all the products price, clean them and store them.
        products = response.css('div.product-card__info')
        store = products.css('div.product-card__price::text').getall()
        
        temp_price = []
        for item in store:
            item_price = item.replace('\n', '').strip()
            # item_price = item_price.replace(' ', '')
            if item_price != "":  
                temp_price.append(item_price)


        # Fetch all the products image link and store them.
        img_links = []
        for line in response.css('noscript img::attr("src")').getall():
            target = 'https:' + line
            img_links.append(target)


        # Fetch all the products name and store them.
        i=0
        for products in response.css('div.product-card__info'):

            yield {
                'link': img_links[i],
                'name': products.css('div.product-card__name::text').get().strip(),
                'price': temp_price[i],
            }
            if(i < len(temp_price)-1):
                i = i+1


        img_names = []
        for products in response.css('div.product-card__info'):
            name = products.css('div.product-card__name::text').get().strip()
            img_names.append(name)

        # Crawl the remaining pages of the website. 
        link = 'https://santrapub.com/'
        if(response.css('span.next a::attr("href")').get() != None):
            next_page = link + response.css('span.next a::attr("href")').get()
        else:
            next_page = link

        if next_page is not link:
            yield response.follow(next_page, callback=self.parse)
