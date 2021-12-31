import scrapy
import json
from scrapy_splash import SplashRequest
import datetime

class NhadatSpider(scrapy.Spider):
    name = 'nhadat247_link'


    
    def start_requests(self):

        script_link = """
                function main(splash, args)
                    splash:init_cookies(splash.args.cookies)
                    assert(splash:go{
                        splash.args.url,
                        headers=splash.args.headers
                    })
                    assert(splash:wait(5))
                    splash:set_viewport_full()
                    local scroll_to = splash:jsfunc("window.scrollTo")
                    local get_body_height = splash:jsfunc(
                        "function() {return document.body.scrollHeight;}"
                    )
                    for _ = 1, 2 do
                        scroll_to(0, get_body_height())
                        assert(splash:wait(1))
                    end 

                    return {
                        headers = last_response.headers,
                        html = splash:html(),
                        url = splash.url()
                    }
                end
            """


        with open('./result/nhadat247/link/link.html', 'w+',encoding='utf-8') as out:
            out.write('')

        link = "https://nhadat247.com.vn"
        yield SplashRequest(
            url=link,
            callback=self.parse,
            session_id="test",
            meta={
                "splash": {
                    "endpoint": "execute", 
                    "args": {
                        "lua_source": script_link,
                    }
                }
            }
        )


    def parse(self, response):
        with open('./result/nhadat247/link/link.html', 'w+',encoding='utf-8') as out:
            out.write(response.text)
        
        h = scrapy.Selector(response)

        try:
            f = open('./result/nhadat247/link/link.json', encoding="utf-8")
            result = json.load(f)
        except json.decoder.JSONDecodeError and FileNotFoundError:
            result = []

        items = h.css("li.khungdo")
        
        index = len(result)

        for item in items:
            i = {}
            i['id'] = index
            index += 1
            i['url'] = 'https://nhadat247.com.vn' + item.css("a").xpath('@href').get()
            i['post_type'] = ""
            i['is_crawled'] = False
            i['error'] = ""
            i['created_at'] = str(datetime.date.today())
            i['updated_at'] = ""
            result.append(i)

        with open('./result/nhadat247/link/link.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
