from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
import scrapy
from scrapy.selector import Selector 
import time
class FirstSpider(scrapy.Spider):
    name = "college2"
    allowed_domains=["https://collegedunia.com/india-colleges"]
    start_urls=[
        "https://collegedunia.com/india-colleges"
    ]
    def __init__ (self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chromepath=which("ch")
        driver = webdriver.Chrome(executable_path=chromepath,options=chrome_options)
        # driver = webdriver.Chrome(executable_path=chromepath)
        driver.get("https://collegedunia.com/india-colleges/")
        last_height = driver.execute_script("return document.body.scrollHeight")
        flag=0
        start_time=time.time()
        while ((time.time() - start_time) < 1*60):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                if (flag>30):
                    break
                flag+=1
                time.sleep(1)
            flag=0
            last_height = new_height
        self.html=driver.page_source
        driver.close()
    def parse(self,response):
        res = Selector(text=self.html) 
        for college in res.css("div.listing-block"):
            name_loc=college.css("div.clg-name-address").css("h3::text").get()
            affiliate=otherdetails=tmp=tmp1=city=state=None
            tmp = college.css("span.location-badge").css("span::text").getall()
            print("------------------------>",tmp)
            if(len(tmp[0].split(","))==2):
                city,state=tmp[0].split(",")
            elif(len(tmp[0].split(","))==1):
                state=tmp[0].split(",")[0]
            elif(len(tmp[0].split(","))==0):
                pass
            else:
                otherdetails=tmp[0]
            if (len(tmp)>2):
                if  (len(tmp[2])!=0):
                    affiliate=tmp[2]
                else:
                    affiliate=None
            
            rating={"collegeduina rateing": college.css("span.rating-text::text").get()}
            for r in college.css("div.media-rank"):
                a=r.css("span.rank-span ::text").get()
                b=r.css("span.rank-span").css("span.rank-name::text").get()
                if (b):
                    rating[b]=a
            tmp1=college.css("ul.clg-fee-review").css("li")
            fees={}
            for a in tmp1: 
                fees[a.css("span.lr-value::text").get()]=a.css("span.lr-key::text").get()
            yield{
                "name_loc":name_loc,
                "city":city,
                "state":state,
                "Affiliate":affiliate,
                "OtherDetails":otherdetails,
                "fees":fees,
                "rating":rating,
                # "courses":courses,
            }