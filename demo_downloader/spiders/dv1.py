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
    name = 'dv1'
    start_urls = ['https://www.xnxx.com']
   
    def parse(self,response):
        # chrome_options = Options()
        # chromepath=which("ch")
        # driver = webdriver.Chrome(executable_path=chromepath,options=chrome_options)
        #             ChromeOptions options = new ChromeOptions()
        # options.addArguments("--headless", "--disable-gpu", "--window-size=1920,1200","--ignore-certificate-errors","--disable-extensions","--no-sandbox","--disable-dev-shm-usage");
        # WebDriver driver = new ChromeDriver(options)
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-gpu")
        #chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.headless = True # also works
        chromepath=which("ch")
        driver = webdriver.Chrome(executable_path=chromepath,options=chrome_options)
        i=1
        j=0
        while(j<1):

            driver.get("https://www.xnxx.com/pornstars/"+str(j))
            j+=1
            res=driver.page_source            
            res=Selector(text=res)
            for college in res.css("div.thumb"):
                print( response.urljoin(college.css("a::attr(href)").extract()[0]) )
                yield scrapy.Request(
                            url=response.urljoin(college.css("a::attr(href)").extract()[0] ),
                            callback=self.parse_page,
                            meta={"c_d":college.css("a::attr(href)").extract_first()}
                        )
                i+=1
                print("------------------main--tabs--no in page crawled:"+str(i)+","+str(j-1))
    def parse_page(self,response):
        c_d=response.request.meta["c_d"]
        i=0
        response.meta
        # for college in response.xpath("//div[contains(@id,'psvideos')] /div/ div[contains(@class,'thumb-block') ]"):
        college = response.xpath("//div[contains(@id,'psvideos')] /div/ div[contains(@class,'thumb-block') ]")[0]
        if college:
            try :
                print(response.urljoin(college.xpath("./a/@href").extract()[0]))
                yield scrapy.Request(
                    url=response.urljoin(college.xpath("./a/@href").extract()[0]),
                    callback=self.parse_information,
                    meta={"c_d":c_d,}
                    )
                i+=1
            except:
                print("skiped")
            # time.sleep(1)
            # print("-------------------------no in page crawled:"+str(i))
        # next_page = response.css('a.no-page.next::attr(href)').get()
        # if (next_page is not None):
        #     yield response.follow(next_page, callback=self.parse) 

    def parse_information(self,response):
        c_d=response.request.meta["c_d"]    
        a=response.xpath("//div[ contains(@id,'video-player-bg') ]/script[4]/text()").extract()[0]
        if( "High" in re.split("\n",a)[8]):
            link=re.split("'",re.split("\n",a)[8])[1]
        elif ("Low" in re.split("\n",a)[7]):
            link=re.split("'",re.split("\n",a)[7])[1]
        # url=re.split("'",re.split("\n",response.xpath("//div[ contains(@id,'video-player-bg') ]/script[4]/text()").extract()[0])[7])[1]
        print(link)
        #regrex to find the url from the script 

        # print("**************************************************************")
        # print(link)
        # print("**************************************************************")
        yield {
         'file_urls': [link],
         'name': response.css("strong::text").get(),
         'res':c_d
        }   