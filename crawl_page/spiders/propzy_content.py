import scrapy
import json
from scrapy_splash import SplashRequest
import datetime

class propzySpider(scrapy.Spider):
    name = 'propzy_content'


    
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


        with open('./result/propzy/content/content.html', 'w+',encoding='utf-8') as out:
            out.write('')
        
        try:
            f = open('./result/propzy/link/link.json', encoding="utf-8")
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

        with open('./result/propzy/link/link.json', 'w', encoding='utf-8') as f:
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
        with open('./result/propzy/content/content.html', 'w+',encoding='utf-8') as out:
            out.write(response.text)

        try:
            f = open('./result/propzy/content/content.json', encoding="utf-8")
            item = json.load(f)
        except json.decoder.JSONDecodeError and FileNotFoundError:
            item = []

        index = len(item)

        h = scrapy.Selector(response)
        result = {}
        result['id'] = index
        result['website'] = response.url.split('.vn')[0] + '.vn'
        result['url'] = response.url
        result['url_type'] = response.url.split('://')[0]
        result['post_type'] = h.css("#wrapper > div.sec-breadcrumbs > div > div > span ::text").extract_first()
        result['post_title'] = h.css("#main > div > div > div:nth-child(1) > div.row.list-item.t-detail-s > div.col-lg-8 > div.t-detail > h1::text").extract_first()
        result['price_unit'] = ""
        result['price'] = h.css("#main > div > div > div:nth-child(1) > div.row.list-item.t-detail-s > div.col-lg-8 > div.t-detail > div.p-price-n::text").extract_first()
        result['total_size_area'] = h.css("#main > div > div > div:nth-child(1) > div.row.list-item.t-detail-s > div.col-lg-8 > div.bl-parameter-listing > ul > li:nth-child(3) > span.sp-info::text").extract_first()
        result['property_name'] = ""
        result['address_id'] = h.css("#main > div > div > div:nth-child(1) > div.row.list-item.t-detail-s > div.col-lg-8 > div.t-detail > p.p-address ::text").extract()[0]
        result['number_of_bedrooms'] =  h.css("#tab-detail > div > ul:nth-child(1) > li:nth-child(1) > span.sp-info ::text").extract()[0]
        result['number_of_bathrooms'] = h.css("#tab-detail > div > ul:nth-child(1) > li:nth-child(2) > span.sp-info ::text").extract_first()
        result['project_id'] = h.css("#main > div > div > div:nth-child(1) > div.row.list-item.t-detail-s > div.col-lg-8 > div.t-detail > div.label.mb-10 > span.label-3::text").extract_first().split(' ')[1]
        result['project_size'] = ""
        result['post_author'] = ""
        result['property_code'] = ""
        result['full_description'] = " ".join(h.css("#tab-overview > div > div ::text").extract())
        result['phone_number'] = ""
        result['email'] = ""
        result['property_type_id'] = ""
        result['property_sub_type_id'] = ""
        result['block_code'] = ""
        result['block_name'] = ""
        result['number_of_floors'] = h.css("#tab-detail > div > ul:nth-child(1) > li:nth-child(6) > span.sp-info ::text").extract()[0]
        result['floor'] = ""
        result['house_design'] = ""
        result['direction'] = h.css("#tab-detail > div > ul:nth-child(1) > li:nth-child(3) > span.sp-info ::text").extract_first()
        result['building_area'] = h.css("#tab-detail > div > ul.ul-introduce.col-md-5.float-right > li:nth-child(1) > span.sp-info ::text").extract_first()
        result['carpet_area'] = h.css("#tab-detail > div > ul.ul-introduce.col-md-5.float-right > li:nth-child(2) > span.sp-info ::text").extract_first()
        result['unit_of_measure_id'] = ""
        result['owner_is_author'] = ""
        result['owner_id'] = ""
        result['longtitude'] = h.css("#tab-detail > div > ul.ul-introduce.col-md-5.float-right > li:nth-child(3) > span.sp-info ::text").extract_first()
        result['latitude'] = h.css("#tab-detail > div > ul.ul-introduce.col-md-5.float-right > li:nth-child(4) > span.sp-info ::text").extract_first()
        result['legal_info'] = h.css("#tab-detail > div > ul:nth-child(1) > li:nth-child(5) > span.sp-info::text").extract_first().replace("\n","")
        result['internal_facility'] = ""
        result['near_facility'] = ""
        result['front_facility'] = h.css("#tab-detail > div > ul.ul-introduce.col-md-5.float-right > li:nth-child(6) > span.sp-info::text").extract_first().replace("\n","").replace(" ","")
        result['route_length'] = h.css("#tab-detail > div > ul.ul-introduce.col-md-5.float-right > li:nth-child(5) > span.sp-info::text").extract_first().replace("\n","").replace(" ","")
        
        

        result['created_at'] = ""
        result['updated_at'] = ""
        result['expired_at'] = ""
        result['is_called_api'] = ""

        result['image'] = h.css("a.img.tRes_60 > img").xpath('@src').extract()

        result['city'] = result['address_id'].split(',')[3] if len(result['address_id'].split(',')) == 4 else ""
        result['district'] = result['address_id'].split(',')[2]
        result['ward_commune'] = result['address_id'].split(',')[1]
        result['street'] = result['address_id'].split(',')[0]
        result['match_location'] = ""
        result['html'] = ""#response.text


        item.append(result)
        with open('./result/propzy/content/content.json', 'w', encoding='utf-8') as f:
            json.dump(item, f, ensure_ascii=False, indent=4)