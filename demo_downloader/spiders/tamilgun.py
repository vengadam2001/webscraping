import scrapy
# import time
# import selenium
# from    shutil                             import which
# from    scrapy.selector                    import Selector 
# from    selenium                           import webdriver
# from    selenium.webdriver.chrome.options  import Options
# from scrapy.loader import ItemLoader
# from demo_downloader import DemoDownloaderItem

#Start url
#  fetch("https://1tamilgun.com/categories/hd-movies/")
# 2020-12-03 13:15:34 [scrapy.core.engine] INFO: Spider opened
# 2020-12-03 13:15:36 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://1tamilgun.com/categories/hd-movies/> (referer: None)


# >>> a=response.css("article header div.rocky-effect div div div a::attr('href')").getall()
# >>> for i in a:
# ...     print(i)

# list of movie div block urls

# >>> fetch(a[0])
# 2020-12-03 13:17:17 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://1tamilgun.com/video/kalki/> (referer: None)
# >>> response.css("div.ts-video iframe::attr(src)").get()
# 'https://cdn.jwplayer.com/players/4nDT00QD-GI6pG8Lp.html'
# >>> b=response.css("div.ts-video iframe::attr(src)").get()
# >>> fetch(b)

# javascript needed....
# 2020-12-03 13:19:14 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://cdn.jwplayer.com/players/4nDT00QD-GI6pG8Lp.html> (referer: None)
# >>> response.css("video")
# []
# >>> response.css("div.jw-media")
# []
# >>> view(response)
# True
# >>> cd ..
#   File "<console>", line 1
#     cd ..
#         ^
# SyntaxError: invalid syntax
# >>> view(response)
# True
# >>>

#for tami.mv 
#responsexpath("//strong/a[@Class='ipsAttachLink']/span")

class tamilmvSpider(scrapy.Spider):
    name = 'tamilmv'
    start_urls = ["https://www.1tamilmv.ws/index.php?/forums/forum/11-web-hd-itunes-hd-bluray/"]
    def parse(self,response):
        count=0
        for movie in response.xpath("//li[@class='ipsDataItem ipsDataItem_responsivePhoto   ']/*/*/div[@class='ipsType_break ipsContained']"):
            count+=1
            yield scrapy.Request(
                        url=response.urljoin(movie.css('a::attr(href)').get()),
                        callback=self.parse_page,
                        meta={"name":movie.xpath('./a/span/text()').get().replace('\n','').replace('\t','').split(' - ')[0]}
            )
        next_p=response.xpath("//a[@rel='next']")[0].css("::attr(href)").get()
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("page no:"+str(count))
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        if (next_p is not None):
            yield response.follow(next_p, callback=self.parse) 

    def parse_page(self,response):
        count=0
        a=response.xpath("//a[@class='ipsAttachLink']")
        if a == None:
            a=response.css("p span a")
        for i in a:
            if 'GB' in i.xpath('./*/text()').get():
                if float(i.xpath('./*/text()').get().split('GB')[0].split(' ')[len(i.xpath('./*/text()').get().split('GB')[0].split(' '))-1]) :
                    if float(i.xpath('./*/text()').get().split('GB')[0].split(' ')[len(i.xpath('./*/text()').get().split('GB')[0].split(' '))-1])<=1.6 and '1080p' in i.xpath('./*/text()').get().split('GB')[0].split(' '):
                        print(i.css("::attr(href)").get())
                        count=count+1
                        yield {
                        'file_urls': [i.css("::attr(href)").get()],
                        'name':response.meta['name'],
                        'res':'1080p'
                        }
                        print("!-||-!!-||-!!-||-!!-||-!!-||-!!-||-!Success")
                        break
                elif float(i.xpath('./*/text()').get().split('GB')[0].split('[')[len(i.xpath('./*/text()').get().split('GB')[0].split('['))-1])<=1.6 and '1080p' in i.xpath('./*/text()').get().split('GB')[0].split(' '):
                        print(i.css("::attr(href)").get())
                        count=count+1
                        yield {
                        'file_urls': [i.css("::attr(href)").get()],
                        'name':response.meta['name'],
                        'res':'1080p'
                        }
                        print("!-||-!!-||-!!-||-!!-||-!!-||-!!-||-!Success")
                        break
                else:
                    print('hello')
            elif 'MB' in i.xpath('./*/text()').get():
                if float(i.xpath('./*/text()').get().split('MB')[0].split(' ')[len(i.xpath('./*/text()').get().split('MB')[0].split(' '))-1])<=1.6 and '1080p' in i.xpath('./*/text()').get().split('GB')[0].split(' '):
                    print(i.css("::attr(href)").get())
                    count=count+1
                    yield {
                    'file_urls': [i.css("::attr(href)").get()],
                    'name':response.meta['name'],
                    'res':'1080p'
                    }
                    break
                elif float(i.xpath('./*/text()').get().split('MB')[0].split('[')[len(i.xpath('./*/text()').get().split('MB')[0].split('['))-1])<=1.6 and '1080p' in i.xpath('./*/text()').get().split('MB')[0].split(' '):
                        print(i.css("::attr(href)").get())
                        count=count+1
                        yield {
                        'file_urls': [i.css("::attr(href)").get()],
                        'name':response.meta['name'],
                        'res':'1080p'
                        }
                        print("!-||-!!-||-!!-||-!!-||-!!-||-!!-||-!Success")
                        break
                else:
                    print('hello')
            else:
                yield {
                        'file_urls': [i.css("::attr(href)").get()],
                        'name':response.meta['name'],
                        'res':'unknown'
                        }
        if count==0:
            try:
                print( response.xpath("//a[@class='ipsAttachLink']").getall() )
                print(response.xpath("//a[@class='ipsAttachLink']")[0].css("::attr(href)").get())
                yield {
                        'file_urls': [response.xpath("//a[@class='ipsAttachLink']")[0].css("::attr(href)").get()],
                        'name':response.meta['name'],
                        'res':'1080p'
                        }
            except Exception as e:
                print( response.xpath("//strong/a").getall() )
                print(response.xpath("//strong/a").css("::attr(href)").getall())
                yield {
                        'file_urls': response.xpath("//strong/a").css("::attr(href)").getall(),
                        'name':response.meta['name'],
                        'res':'1080p'
                        }