import scrapy
import time
import selenium
from    shutil                             import which
from    scrapy.selector                    import Selector 
from    selenium                           import webdriver
from    selenium.webdriver.chrome.options  import Options
import re
# from scrapy.loader import ItemLoader
# from demo_downloader import DemoDownloaderItem
class DvSpider(scrapy.Spider):
    name = 'dv3'
    start_urls = ['http://wikipedia.com']
   
    def parse(self,response):
        # chrome_options = Options()
        # chromepath=which("ch")
        # driver = webdriver.Chrome(executable_path=chromepath,options=chrome_options)
        #             ChromeOptions options = new ChromeOptions()
        # options.addArguments("--headless", "--disable-gpu", "--window-size=1920,1200","--ignore-certificate-errors","--disable-extensions","--no-sandbox","--disable-dev-shm-usage");
        # WebDriver driver = new ChromeDriver(options)
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.headless = True # also works
        # chrome_options.add_argument("--disable-gpu")
        #chrome_options.add_argument("--no-sandbox") # linux only
        chromepath=which("ch")
        driver = webdriver.Chrome(executable_path=chromepath,options=chrome_options)
        links=[
            'https://www.amazon.in/HP-16-1-inch-Graphics-Flicker-16-e0078AX/product-reviews/B098QB5VW3/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=',
            'https://www.amazon.in/HP-Pavilion-Processor-15-6-inch-15-dk1508TX/product-reviews/B08ZN6KNP1/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=',
            'https://www.amazon.in/ASUS-i5-10300H-Graphics-Fortress-FX566LH-HN257T/product-reviews/B08CRMTKMK/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=',
            'https://www.amazon.in/ASUS-15-6-inch-RTX-3050-Graphics-FA506IC-HN005T/product-reviews/B09CCW5XVM/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=',
            'https://www.amazon.in/HP-Pavilion-Processor-15-6-inch-15-dk1148TX/product-reviews/B091FJ5WPQ/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=',
            'https://www.amazon.in/HP-16-1-inch-Graphics-Flicker-16-e0078AX/product-reviews/B098QB5VW3/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=',
            'https://www.amazon.in/Lenovo-IdeaPad-Windows-Graphics-81Y40183IN/product-reviews/B096SK39ZB/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=',
            'https://www.amazon.in/Lenovo-IdeaPad-Windows-Graphics-82EY00U4IN/product-reviews/B096SKGTCG/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=',
]
        for k in links:
            j=1
            reviews=""
            while j<1000:
                flag=0
                driver.get(k+str(j))
                res=driver.page_source            
                res=Selector(text=res)
                j+=1
                name=res.xpath('//a[@class="a-link-normal"]/text()[1]').get()
                if len(res.xpath("//div[@class='a-section review aok-relative']"))<1:
                    break
                for i in res.xpath("//div[@class='a-section review aok-relative']"):
                    print(i.xpath('./div/div/div[4]/span/span/text()').get())
                    print(i.xpath('./div/div/span/text()').get())
                
                    reviews = reviews +"   "+str(i.xpath('./div/div/div[4]/span/span/text()').get())
                if flag ==1:
                    break
            yield {
                        'comment': reviews,
                        'name': name,
                    }