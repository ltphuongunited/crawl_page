import scrapy
import json
from scrapy_splash import SplashRequest
import datetime

class ChototSpider(scrapy.Spider):
    name = 'chotot_content'


    hide_phone = "sc-bZQynM ijabWE"

    
    def start_requests(self):

        script_link = """
                function main(splash, args)
                    splash:init_cookies(splash.args.cookies)
                    assert(splash:go{
                        splash.args.url,
                    })
                    assert(splash:wait(5))

                    splash:select('button[class=login]'):mouse_click()
                    assert(splash:wait(math.random(0,1)))
                    
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


        with open('./result/chotot/content/content.html', 'w+',encoding='utf-8') as out:
            out.write('')
        
        try:
            f = open('./result/chotot/link/link.json', encoding="utf-8")
            links = json.load(f)
        except json.decoder.JSONDecodeError and FileNotFoundError:
            links = []
        
        if len(links) == 0:
            return

        link_crawl = []
        for link in links:
            if link['is_crawled'] == False:
                link_crawl.append(link['url'])
                link['is_crawled'] = True

        with open('./result/chotot/link/link.json', 'w', encoding='utf-8') as f:
            json.dump(links, f, ensure_ascii=False, indent=4)


        for link in link_crawl:
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
        with open('./result/chotot/content/content.html', 'w+',encoding='utf-8') as out:
            out.write(response.text)
        try:
            f = open('./result/chotot/content/content.json', encoding="utf-8")
            item = json.load(f)
        except json.decoder.JSONDecodeError and FileNotFoundError:
            item = []

        index = len(item)

        h = scrapy.Selector(response)
        result = {}
        result['id'] = index
        result['website'] = response.url.split('.com')[0] + '.com'
        result['url'] = response.url
        result['url_type'] = response.url.split('://')[0]
        result['post_type'] = h.css("div.ct-detail.adview > div > div.row > div.col-sm-8 > div > div > ol > li:nth-child(2) > a > span ::text").extract()
        result['post_title'] = h.css("#__next > div.container > div.ct-detail.adview > div > div.col-md-8 > div.AdDecription_adDecriptionWrapper__36qgN > h1 ::text").extract()[1]
        result['price_unit'] = ""
        result['price'] = h.css("#__next > div.container > div.ct-detail.adview > div > div.col-md-8 > div.AdDecription_adDecriptionWrapper__36qgN > div.AdDecription_priceWrapper__38i3q > div.AdDecription_adPrice__1Ps8j > span > div > span > span > span:nth-child(1)::text").extract_first()
        result['total_size_area'] = h.css("#__next > div.container > div.ct-detail.adview > div > div.col-md-8 > div.AdDecription_adDecriptionWrapper__36qgN > div.AdDecription_priceWrapper__38i3q > div.AdDecription_adPrice__1Ps8j > span > div > span > span > span:nth-child(1) > span::text").extract()[1]
        result['property_name'] = ""
        result['address_id'] = h.css("span.fz13 ::text").extract()
        result['number_of_bedrooms'] =  ""
        result['number_of_bathrooms'] = ""
        result['project_id'] = ""
        result['project_size'] = ""
        result['post_author'] = h.css("div.SellerProfile_nameDiv__dd88e b::text").extract_first()
        result['property_code'] = ""
        result['full_description'] = h.css("#__next > div.container > div.ct-detail.adview > div > div.col-md-8 > div.AdDecription_adDecriptionWrapper__36qgN > p ::text").extract()[0]
        result['phone_number'] = h.css("div.sc-bZQynM.ijabWE > span ::text").extract()
        result['email'] = ""
        result['property_type_id'] = h.css("#__next > div.container > div.ct-detail.adview > div > div.col-md-8 > div:nth-child(5) > div:nth-child(11) > div > div.media-body.media-middle > span > span.AdParam_adParamValue__1ayWO ::text").extract()[0]
        result['property_sub_type_id'] = ""
        result['block_code'] = ""
        result['block_name'] = ""
        result['number_of_floors'] = ""
        result['floor'] = ""
        result['house_design'] = h.css("#__next > div.container > div.ct-detail.adview > div > div.col-md-8 > div:nth-child(5) > div:nth-child(6) > div > div.media-body.media-middle > span > span.AdParam_adParamValue__1ayWO ::text").extract()[0]
        result['direction'] = h.css("#__next > div.container > div.ct-detail.adview > div > div.col-md-8 > div:nth-child(5) > div:nth-child(4) > div > div.media-body.media-middle > span > span.AdParam_adParamValue__1ayWO ::text").extract()[0]
        result['building_area'] = h.css("#__next > div.container > div.ct-detail.adview > div > div.col-md-8 > div:nth-child(5) > div:nth-child(2) > div > div.media-body.media-middle > span > span.AdParam_adParamValue__1ayWO ::text").extract()[0]
        result['carpet_area'] = ""
        result['unit_of_measure_id'] = ""
        result['owner_is_author'] = ""
        result['owner_id'] = ""
        result['longtitude'] = h.css("#__next > div.container > div.ct-detail.adview > div > div.col-md-8 > div:nth-child(5) > div:nth-child(13) > div > div.media-body.media-middle > span > span.AdParam_adParamValue__1ayWO ::text").extract()[0]
        result['latitude'] = h.css("#__next > div.container > div.ct-detail.adview > div > div.col-md-8 > div:nth-child(5) > div:nth-child(12) > div > div.media-body.media-middle > span > span.AdParam_adParamValue__1ayWO ::text").extract()[0]
        result['legal_info'] = h.css("#__next > div.container > div.ct-detail.adview > div > div.col-md-8 > div:nth-child(5) > div:nth-child(5) > div > div.media-body.media-middle > span > span.AdParam_adParamValue__1ayWO ::text").extract_first()
        result['internal_facility'] = ""
        result['near_facility'] = ""
        result['front_facility'] = ""
        result['route_length'] = ""
    

        result['created_at'] = ""
        result['updated_at'] = ""
        result['expired_at'] = ""
        result['is_called_api'] = ""

        result['image'] = h.css("div.AdImage_sliderWrapper__GkjAp img").xpath('@src').extract()

        result['city'] = ""
        result['district'] = ""
        result['ward_commune'] = ""
        result['street'] = ""
        result['match_location'] = ""
        result['html'] = ""#response.text


        item.append(result)
        with open('./result/chotot/content/content.json', 'w', encoding='utf-8') as f:
            json.dump(item, f, ensure_ascii=False, indent=4)

