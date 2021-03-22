import scrapy
import time
import selenium
from    shutil                             import which
from    scrapy.selector                    import Selector 
from    selenium                           import webdriver
from    selenium.webdriver.chrome.options  import Options
# from scrapy.loader import ItemLoader
# from demo_downloader import DemoDownloaderItem
class DvSpider(scrapy.Spider):
    name = 'fmb'
    start_urls = ['https://collabland-tn.gov.in/FMBMapService.jsp?state=33&giscode=0107018']
    def parse(self,response):
        i=1
        chrome_options = Options()
        chromepath=which("ch")
        driver = webdriver.Chrome(executable_path=chromepath,options=chrome_options)
        driver.get("https://collabland-tn.gov.in/FMBMapService.jsp?state=33&giscode=0107018"+str(i))
        res=driver.page_source
        res=Selector(text=res)
        while i<438:
            try:
                #437
                link = res.css('embed::attr(src)').get()
                yield {
                'file_urls': [link],
                'name':"survey number : "+str(i)
                }
                print("-------------------------no in page crawled:"+str(i))

            except Exception as e:
                print(e)
                print("skipped")

            finally:
                if (res is not None) and (i<10):
                    driver.get("https://collabland-tn.gov.in/FMBMapService.jsp?state=33&giscode=0107018"+str(i))
                    time.sleep(1)
                    res=driver.page_source
                    res=Selector(text=res)
                    i+=1
                else:
                    break