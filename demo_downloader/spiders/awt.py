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
    name = "awt"
    start_urls = ['http://wikipedia.com']
   
    def parse(self,response):
        link='https://www.amazon.in/pay/history?ref_=apay_deskhome_ViewStatement'
        inputs=[
            {
                "username":"7904838873",
                "password":"Vengadam@2003"
            },
            {
                "username":"sadasivam73@gmail.com",
                "password":"Vengadam@2003"
            },
            ]
        # chrome_options = Options()
        # chromepath=which("ch")
        # driver = webdriver.Chrome(executable_path=chromepath,options=chrome_options)
        #             ChromeOptions options = new ChromeOptions()
        # options.addArguments("--headless", "--disable-gpu", "--window-size=1920,1200","--ignore-certificate-errors","--disable-extensions","--no-sandbox","--disable-dev-shm-usage");
        # WebDriver driver = new ChromeDriver(options)
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.headless = True # also works
        # chrome_options.add_argument("--disable-gpu")
        #chrome_options.add_argument("--no-sandbox") # linux only
        chromepath=which("ch")
        driver = webdriver.Chrome(executable_path=chromepath,options=chrome_options)
        for j in inputs:
            driver.get(link)
            driver.find_element_by_xpath("//input[@id='ap_email']").send_keys(j["username"])
            driver.find_element_by_xpath("//input[@id='ap_password']").send_keys(j["password"])
            driver.find_element_by_xpath("//input[@id='signInSubmit']").click()
            time.sleep(10)
            print(input("confirm after otp"))
            res=driver.page_source            
            res=Selector(text=res)
            divs=res.xpath("//div[@id='transaction-desktop']/a/span/div/div/div/div[@class='a-row']")
            i=0
            print(len(divs))
            while i < len(divs):
                tim         =divs[i].xpath("./div[1]/span/text()").get().replace("\n","").replace("  ","")          #time
                amount      =divs[i].xpath("./div[2]/span/text()").get().replace("\n","").replace("  ","")          #amount
                title       =divs[i].xpath("./div[1]/div[1]/span/text()").get().replace("\n","").replace("  ","")   #title
                pay_method  =divs[i].xpath("./div[1]/div[2]/span/text()").get().replace("\n","").replace("  ","")   #pay_method
                # print("------------------------------------------------------------")
                
                # print(divs[3].xpath("//div[@id='transaction-desktop']/a/span/div/div/div/div[@class='a-row']/div[2]/span/text()").get())
                # print(i.xpath('./div/div/span/text()').get())
                i+=1
                yield {
                    'title': title ,
                    'pay_method': pay_method,
                    'time':tim,
                    'amount':amount,
                    'username':j["username"]
                }   
            driver.get("https://www.amazon.in/gp/flex/sign-out.html?path=%2Fgp%2Fyourstore%2Fhome&useRedirectOnSuccess=1&signIn=1&action=sign-out&ref_=nav_AccountFlyout_signout")