import scrapy
import json
from scrapy_splash import SplashRequest
import datetime

class NhadatSpider(scrapy.Spider):
    name = 'nhadat247_content'

    
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


        with open('./result/nhadat247/content/content.html', 'w+',encoding='utf-8') as out:
            out.write('')
        
        try:
            f = open('./result/nhadat247/link/link.json', encoding="utf-8")
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

        with open('./result/nhadat247/link/link.json', 'w', encoding='utf-8') as f:
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
        with open('./result/nhadat247/content/content.html', 'w+',encoding='utf-8') as out:
            out.write(response.text)
        try:
            f = open('./result/nhadat247/content/content.json', encoding="utf-8")
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
        result['post_type'] = h.css("body > div.menu.fix > div > ul > li.lv0.active > a::text").extract_first()
        result['post_title'] = h.css("body > div.wr_page > div.index-page > div > div.content-left > div.product-detail > h1::text").extract_first().replace("\n","")
        result['price_unit'] = ""
        result['price'] = h.css("#ContentPlaceHolder1_ProductDetail1_divprice > span.spanprice::text").extract_first().replace("\n","").replace(" ","")
        result['total_size_area'] = h.css("#ContentPlaceHolder1_ProductDetail1_divprice > span:nth-child(2)::text").extract_first().replace("\n","").replace(" ","")
        result['property_name'] = ""
        result['address_id'] = "-".join(h.css("#ContentPlaceHolder1_ProductDetail1_divlocation > a::text").extract())
        result['number_of_bedrooms'] =  ""
        result['number_of_bathrooms'] = h.css("div.pd-dacdiem #tbl1 tr:nth-child(9) td:nth-child(2) ::text").extract_first().replace("\n","").replace(" ","")
        result['project_id'] = h.css("#ContentPlaceHolder1_ProductDetail1_divprice > div > span::text").extract_first()
        result['project_size'] = ""
        result['post_author'] = h.css("div.pd-contact #tbl2 tr:nth-child(1) td:nth-child(2) b ::text").extract_first()
        result['property_code'] = ""
        result['full_description'] = ''.join(h.css("div.pd-desc-content ::text").extract()).replace(''.join(h.css("div.xemso ::text").extract()),"").replace("\n","")
        result['phone_number'] = h.css("div.xemso a.hide ::text").extract_first().replace(" ", "")
        result['email'] = h.css("div.pd-contact #tbl2 tr:nth-child(6) td:nth-child(2) ::text").extract_first().replace("\n","").replace(" ","")
        result['property_type_id'] = h.css("div.pd-dacdiem #tbl1 tr:nth-child(1) td:nth-child(2) ::text").extract_first().replace("\n","")
        result['property_sub_type_id'] = ""
        result['block_code'] = ""
        result['block_name'] = ""
        result['number_of_floors'] = h.css("div.pd-dacdiem #tbl1 tr:nth-child(8) td:nth-child(2) ::text").extract_first().replace("\n","").replace(" ","")
        result['floor'] = ""
        result['house_design'] = ""
        result['direction'] = ""
        result['building_area'] = ""
        result['carpet_area'] = ""
        result['unit_of_measure_id'] = ""
        result['owner_is_author'] = ""
        result['owner_id'] = ""
        result['longtitude'] = ""
        result['latitude'] = ""
        result['legal_info'] = h.css("div.pd-dacdiem #tbl1 tr:nth-child(2) td:nth-child(2)::text").extract_first().replace("\n","")
        result['internal_facility'] = ""
        result['near_facility'] = ""
        result['front_facility'] = h.css("div.pd-dacdiem #tbl1 tr:nth-child(7) td:nth-child(2)::text").extract_first().replace("\n","").replace(" ","")
        result['route_length'] = h.css("div.pd-dacdiem #tbl1 tr:nth-child(6) td:nth-child(2)::text").extract_first().replace("\n","").replace(" ","")
        
        created_at = "".join(h.css("#ContentPlaceHolder1_ProductDetail1_divprice > div ::text").extract())
        if "hôm nay" in created_at:
            created_at = str(datetime.date.today())
            
        elif "hôm qua" in created_at:
            created_at = str(datetime.date.today() - datetime.timedelta(days=1))

        else:
            created_at = created_at.split("|")[1].replace('\n',"").replace("\t","").replace(" ","")
            created_at = str(datetime.datetime.strptime(created_at, '%d/%m/%Y')).split(' ')[0]
        

        result['created_at'] = created_at
        result['updated_at'] = ""
        result['expired_at'] = ""
        result['is_called_api'] = ""

        result['image'] = [result['website'] + x for x in h.css("div.pd-slide img").xpath('@src').getall()]

        result['city'] = h.css("#ContentPlaceHolder1_ProductDetail1_divlocation > a:nth-child(5)::text").extract_first()
        result['district'] = h.css("#ContentPlaceHolder1_ProductDetail1_divlocation > a:nth-child(4)::text").extract_first()
        result['ward_commune'] = h.css("#ContentPlaceHolder1_ProductDetail1_divlocation > a:nth-child(3)::text").extract_first().split('Phường ')[-1]
        result['street'] = h.css("#ContentPlaceHolder1_ProductDetail1_divlocation > a:nth-child(2)::text").extract_first().split('đường ')[-1]
        result['match_location'] = ""
        result['html'] = ""#response.text

        item.append(result)
        with open('./result/nhadat247/content/content.json', 'w', encoding='utf-8') as f:
            json.dump(item, f, ensure_ascii=False, indent=4)
