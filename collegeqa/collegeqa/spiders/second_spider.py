import scrapy
class FirstSpider(scrapy.Spider):
    name = "college1"
    start_urls=[
        "https://www.indcareer.com/find/all-colleges"
    ]
    def parse(self,response):
        for college in response.css("div.media"):
            name=college.css("h4").css("a::text").get()
            grp_aff=college.css("small::text").getall()
            cs=college.css("span::text").getall()
            if (len(cs) == 2):
                city,state=cs
            elif (len(cs) == 1):
                state=cs[0]
                city=''
            else:
                state=''
                city=''   
            coruses=college.css("ul.list-unstyled").css("li::text").getall()

            yield{
                "name":name,
                "grp_affi":grp_aff,
                "city":city,
                "state":state,
                "coruses":coruses,
            }
        next_page = response.css('li.pager-next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)