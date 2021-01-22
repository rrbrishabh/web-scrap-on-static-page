import scrapy


class QuotesSpider(scrapy.Spider):
    name = "blue_tomato"
  #  allowed_domains = ["https://www.blue-tomato.com/en-IN/products/categories/Snowboard+Shop-00000000/gender/men"]
    start_urls = ["https://www.blue-tomato.com/de-AT/products/categories/Snowboard+Shop-00000000/gender/men/",
                  "https://www.blue-tomato.com/de-AT/products/categories/Snowboard+Shop-00000000/gender/women/",
                  "https://www.blue-tomato.com/de-AT/products/categories/Snowboard+Shop-00000000/gender/girls/",
                  "https://www.blue-tomato.com/de-AT/products/categories/Snowboard+Shop-00000000/gender/boys/"]

    def parse(self, response):
        # for loop for main url 
        for product_details in response.xpath("//section[@id='productList']/ul/li[starts-with(@id, 'p')]"):
            # other part of the url for the brand
            product_Brand = product_details.xpath("span[@class='productdesc']/a/@data-brand").get()
            # for Name
            product_Name = product_details.xpath("span[@class='productdesc']/a/@data-productname").get()
            
            # for price
            product_Price = product_details.xpath("span[@class='productdesc']/span[@class='price sale']/text()").get()
            if product_Price is None:
              product_Price = product_details.xpath("span[@class='productdesc']/span[@class='price']/text()").get()
            # replace ( €) with ()
            product_Price = product_Price.replace("\n        \xa0","") 

            # for product url
            product_url = product_details.xpath("span/a/@href").get()
            # join url with the base url
            product_url = response.urljoin(product_url)

            # for image url
            product_imageurl = product_details.xpath("span[@class='productimage']/img/@data-src").get()
            if product_imageurl is None:
              product_imageurl = product_details.xpath("span[@class='productimage']/img/@src").get()
            # url replace with context
            product_imageurl = product_imageurl.replace("?$b1$","")
     
            # put the value in dictionary with the help of yield
            yield {
                "Brand" : product_Brand,   
                "Name" : product_Name,
                "Price(in Euros €)" : product_Price,
                "Product_Url" : product_url,
                "Image_Url" : product_imageurl
            }

        # follow pagination link here
        next_page = response.xpath("//li[@class='next browse']/a/@href").get()
        self.log(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            self.log("got :")
            yield response.follow(url = next_page, callback= self.parse)






 