from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
import scrapy
from scrapy.selector import Selector 
import time
class FirstSpider(scrapy.Spider):
    name = "college0"
    allowed_domains=["https://www.collegedekho.com/colleges-in-india"]
    start_urls=[
        "https://www.collegedekho.com/engineering/colleges-in-india/"
    ]
    def __init__ (self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chromepath=which("ch")
        driver = webdriver.Chrome(executable_path=chromepath,options=chrome_options)
        driver.get("https://www.collegedekho.com/engineering/colleges-in-india/")
        try:
            while (driver.find_element_by_id('loadMoreButton')):
            # for i in range (0,1000,1):
                run_tab = driver.find_element_by_id('loadMoreButton')
                run_tab.click()
                # time.sleep(2)
        
        except :
            pass
        self.html=driver.page_source
        driver.close()

    def parse(self,response):
        res = Selector(text=self.html) 
        for college in res.css("div.box"):
            name_loc=college.css("div.title").css("a::text").get()
            tmp=college.css("ul.info").css("li::text").getall()
            if(len(tmp)>3):
                Approved_by=tmp.pop(0)
                Type=tmp.pop(0)
                NIRF_Ranking=tmp.pop(0)
                otherdetails=tmp
            elif (len(tmp)==3):
                Approved_by,Type,NIRF_Ranking=tmp
                otherdetails=None
            elif (len(tmp)==2):
                Approved_by,Type=tmp
                otherdetails=NIRF_Ranking=None
            elif (len(tmp)==1):
                Approved_by=tmp[0]
                otherdetails=Type=NIRF_Ranking=None
            else:
                otherdetails=Approved_by=Type=NIRF_Ranking=None    
            if (college.css("ul.links").css("li").css("a::attr(href)").get()):
                courses="https://www.collegedekho.com/"+college.css("ul.links").css("li").css("a::attr(href)").get()
            else:
                courses=None
            yield{
                "name_loc":name_loc,
                "Approved_by":Approved_by,
                "Type":Type,
                "NIRF_Ranking":NIRF_Ranking,
                "OtherDetails":otherdetails,
                "courses":courses,
            }