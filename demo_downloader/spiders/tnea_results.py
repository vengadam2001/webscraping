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
def replaces(a):
    return( a.replace(" ","") )
class DvSpider(scrapy.Spider):
    name = "tnea"
    start_urls = ['http://wikipedia.com']
   
    def parse(self,response):
        link='https://cutoff.tneaonline.org/#res'
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
        driver.get(link)
        driver.find_element_by_xpath("//input[@type='submit']").click()
        time.sleep(5)
        res=driver.page_source            
        res=Selector(text=res)
        headings = res.xpath("//table/thead/tr/th/text()").getall()
        headings=list(map(replaces,headings))
        row=res.xpath("//table/tbody/tr")
        # dic=dict()
        for i in row:
            arr = i.xpath('td/text()').getall()
            dic=dict()
            for j in range(len(arr)):
                dic[ headings[j] ] = arr[j]
            for j in range(len(arr),len(headings)-len(arr)):
                dic[ headings[j] ] = " "
            # print(dic)
            yield dic 
