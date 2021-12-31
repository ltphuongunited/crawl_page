import scrapy
import json
from scrapy_splash import SplashRequest
import datetime

class mogiSpider(scrapy.Spider):
    name = 'mogi_content'


    
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


        with open('./result/mogi/content/content.html', 'w+',encoding='utf-8') as out:
            out.write('')
        
        link = "https://mogi.vn/huyen-nha-be/mua-nha-hem-ngo/nha-so-hong-rieng-hem-2295-huynh-tan-phat-thi-tran-nha-be-3-tang-4pn-id21419202"
        
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

        with open('./result/mogi/content/content.html', 'w+',encoding='utf-8') as out:
            out.write(response.text)

        try:
            f = open('./result/mogi/content/content.json', encoding="utf-8")
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
        result['post_type'] = h.css("#breadcrumb > ul > li:nth-child(2) > a > span::text").extract_first()
        result['post_title'] = h.css("#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.title > h1::text").extract_first()
        result['price_unit'] = ""
        result['price'] = h.css("#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.price::text").extract_first().replace("\n","").replace(" ","")
        result['total_size_area'] = "".join(h.css("#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-attrs.clearfix > div:nth-child(2) > span:nth-child(2)::text").extract())
        result['property_name'] = ""
        result['address_id'] = "-".join(h.css("#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.address::text").extract())
        result['number_of_bedrooms'] =  h.css("#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-attrs.clearfix > div:nth-child(3) > span:nth-child(2) ::text").extract_first()
        result['number_of_bathrooms'] = h.css("#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-attrs.clearfix > div:nth-child(4) > span:nth-child(2) ::text").extract_first()
        result['project_id'] = h.css("#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-attrs.clearfix > div:nth-child(7) > span:nth-child(2) ::text").extract_first()
        result['project_size'] = ""
        result['post_author'] = h.css("#mogi-page-content > div.property-detail.clearfix > div.side-bar > div.agent-widget.widget > div.agent-info > div.agent-name > a::text").extract_first()
        result['property_code'] = ""
        result['full_description'] = ''.join(h.css("#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-content-body ::text").extract())
        result['phone_number'] = h.css("#mogi-page-content > div.property-detail.clearfix > div.side-bar > div.agent-widget.widget > div.agent-contact.clearfix > a:nth-child(1) > span ::text").extract_first()
        result['email'] = ""
        result['property_type_id'] = ""
        result['property_sub_type_id'] = ""
        result['block_code'] = ""
        result['block_name'] = ""
        result['number_of_floors'] = ""
        result['floor'] = ""
        result['house_design'] = ""
        result['direction'] = ""
        result['building_area'] = "".join(h.css("#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-attrs.clearfix > div:nth-child(2) > span:nth-child(2)::text").extract())
        result['carpet_area'] = h.css("#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-attrs.clearfix > div:nth-child(1) > span:nth-child(2) ::text").extract_first()
        result['unit_of_measure_id'] = ""
        result['owner_is_author'] = ""
        result['owner_id'] = ""
        result['longtitude'] = ""
        result['latitude'] = ""
        result['legal_info'] = h.css("#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-attrs.clearfix > div:nth-child(5) > span:nth-child(2)::text").extract_first()
        result['internal_facility'] = ""
        result['near_facility'] = ""
        result['front_facility'] = ""
        result['route_length'] = ""
        
        created_at = h.css("#mogi-page-content > div.property-detail.clearfix > div.property-detail-main > div.main-info > div.info-attrs.clearfix > div:nth-child(6) > span:nth-child(2) ::text").extract_first()
        created_at = str(datetime.datetime.strptime(created_at, '%d/%m/%Y')).split(' ')[0]
        

        result['created_at'] = created_at
        result['updated_at'] = ""
        result['expired_at'] = ""
        result['is_called_api'] = ""

        list_img = list(h.css("div.media-item img").xpath('@data-src').extract())
        img = list(h.css("div.media-item img").xpath('@src').extract())
        result['image'] = img + list_img

        result['city'] = result['address_id'].split(',')[3]
        result['district'] = result['address_id'].split(',')[2]
        result['ward_commune'] = result['address_id'].split(',')[1]
        result['street'] = result['address_id'].split(',')[0]
        result['match_location'] = ""
        result['html'] = ""#response.text


        item.append(result)
        with open('./result/mogi/content/content.json', 'w', encoding='utf-8') as f:
            json.dump(item, f, ensure_ascii=False, indent=4)
