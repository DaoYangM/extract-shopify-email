import json
import re

import regex
import requests
import scrapy
from bs4 import BeautifulSoup
from redis import Redis
from scrapy.utils import spider
from bs4.element import Comment

from extract_shopify_email.settings import DEFAULT_REQUEST_HEADERS

contact_us_res = r'<a .*?href="(.*?)" .*?>contact us</a>'
about_us_res = r'<a .*?href="(.*?)" .*?>about us</a>'
email_rex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
facebook_rex = r'href="(https://www.facebook.com/.*?)"'
twitter_rex = r'href="(https://(www.)?twitter.com/.*?)"'
instagram_rex = r'href="(https://www.instagram.com/.*?)"'

CBK =['AOP+ Easy Print on Demand', 'Fuel: Print on Demand', 'T‑PoP', 'printy6', 'Gooten', 'subliminator', 'shopoo', 'twofifteen', 'kincustom', 'pixels', 'tshirtgang', 'printmelon', 'superfastpod', 'inkthreadable', 'pillowprofits', 'artofwhere', 'creativehub', 'printrove', 'viralstyle', 'gearlaunch', 'tunetoo', 'shirtee', 'skyou', 'rageon', 'teezily', 'printpartners', 'rocketees', 'Customcat', 'spod', 'apliiq', 'WC Fulfillment Print on Demand', 'printaura', 'Printful', 'Printify', 'spocket', 'Zazzle', 'Teefury', 'Teespring', 'Interestprint', 'Forudesigns', 'Customink', 'Spreadshirt', 'CafePress', 'Sunfrog', 'Society6', 'Redbubble', 'Designbyhumans']
BES = ['dropshipping', 'wholesale', 'supplier', 'dropshipper', 'reseller', 'resell']
BEB = ['Chinabrands', 'Boxed', 'Made in China', 'Squarespace', '3dcart', 'oberlo', 'ecomdash', 'dropshippingcms', 'floship', 'ecommercefuel', 'volusion', 'salehoo', 'Dropshippinghelps', 'wholesale2b', 'inventorysource', 'worldwidebrands', 'dropified', 'dhgate', 'doba', 'wholesalecentral', 'sunrisewholesale', 'dropshipnews', 'alidropship', 'alibaba', 'crov', 'modalyst', 'lovelywholesale', 'shopify dropshipping', 'product source']
CK = ['custom', 'customize', 'design', 'create', 'print', 'customized', 'customized shirt', 'customized clothing', 'print on demand', 'design your own', 'printing', 'do it yourself', 'paint', 'made', 'handmade', 'printer', 'embroidered', 't shirt design', 'christmas stockings', 'custom hats', 'custom phone cases', 'custom hoodies', 'wall decals', 'bella canvas', 'casemate', 'christmas tree skirt', 'custom mugs', 'custom socks', 'make your own shirt', 'personalized stockings', 't shirt maker', 'tshirt design', 'weekend bag', 'canvas on demand', 'personalized christmas stockings', 'platform heels', 'spiral notebook', 'case mate', 'custom coffee mugs', 'custom t shirt printing', 'design your own shirt', 'make a shirt', 'personalized christmas ornaments', 'remove background from image', 'skater skirt', 'stainless steel water bottle', 'create a shirt', 'crew socks', 'custom dog tags', 'custom iphone cases', 'custom mouse pads', 'heart shape', 'custom water bottles', 'direct to garment printer', 'gildan hoodies', 'laptop sleeve', 'shipping calculator', 'canvas sizes', 'create your own shirt', 'custom embroidered hats', 'custom t shirts cheap', 'custom tshirt', 'design a shirt', 'embroidered hats', 'face socks', 'mens high top sneakers', 'print on demand', 'rgb color', 'sporttek', 't shirt design online', 't shirt logo', 'tshirt printing', 'bella canvas shirts', 'cheap custom shirts', 'custom canvas prints', 'custom cups', 'custom magnets', 'custom t shirt design', 'dude perfect merch', 'phone case stickers', 'racerback tank', 'socks with faces', 't shirt design maker', 'try guys merch', 'varsity jacket mens', 'custom christmas ornaments', 'diy fit', 'gildan sweatshirts', 'next level t shirts', 'sticker design', 'bella and canvas', 'cgproprints', 'custom made t shirts', 'flat bill hats', 'hooded blanket', 'how to make t shirts', 'lv phone case', 'personalized shirts', 't shirt design template', 'tshirt maker', "women's boxer briefs", 'womens boxer briefs', 'canvas fit', 'ceramic mug', 'custom shirts online', 'custom stockings', 'custom trucker hats', 'custom underwear', 'etsy wholesale', 'face on socks', "flexi", "independent trading company", "my ebay store", "shopify dropshipping", "st patrick's day background", 'stretched canvas', 't shirt design app', 't shirt design website', 't shirt printing online', 'tank tops for girls', 'where does mr beast live', 'white t shirt dress', 'bella canvas 3001', 'canvas shirts', 'canvas t shirts', 'clothes design', 'create stickers', 'custom caps', 'custom christmas stockings', 'custom hoodies cheap', 'custom shirt maker', 'custom tapestry', 'dtg', 'how to make a shirt', 'personalized mouse pads', 'phone case maker', 'reddit pewdiepie', 'rgb vs cmyk', 'sublimation shirts', 't shirt sale', 't shirts online', 'wall art prints', 'yeti stickers', 'yeti tumbler sale', 'alstyle', 'baseball tee shirts', 'bella canvas t shirts', 'cheap t shirt design', 'custom boxers', 'custom sequin pillow', 'custom snapback hats', 'ebay phone cases', 'etsy t shirts', 'fifth sun', 'free t shirt', 'gildan shirt colors', 'how to design a shirt', 'knit beanie', 'lightweight hoodie', 'make shirts online', 'make your own tshirt', 'miranda sings merch', 'mug design', 'my locker', 'next level shirts', 'order t shirts', 'personalized pillow cases', 'personalized travel mugs', 'pom beanie', 'print aura', 'print from phone', 'prodigi', 'shower curtain sizes', 'sport tek shirts', 'tshirt designer', 'varsity jacket womens', 'cg pro prints', 'cmyk color', 'create your own phone case', 'custom coffee cups', 'custom fitted hats', 'custom iphone x case', 'custom phone cases cheap', 'hottest youtubers', 'how does shopify work', 'how to design clothes', 'how to integrate', 'how to make your own t shirt', 'how to start an online store', 'make my own shirt', 'make your own sweatshirt', 'mug printing', 'personalized hats', 'redbubble free shipping', 'sherpa fleece', 'shipping prices', 'vectezzy', 'wix phone number', 'youtube merchandise', 'youtube revenue', 'bag tag', 'bella shirts', 'best color printer', 'best t shirt design website', 'cancel order', 'casemate cases', 'cheap custom phone cases', 'christmas skirt', 'cmyk to rgb', 'contact etsy', 'custom hats no minimum', 'custom photo socks', 'custom products', 'custom tshirt printing', 'customize your own shirt', 'demand meaning', 'design your own tshirt', 'dropshipping reddit']


REDIS_DS_KEY = 'shopify-email'
REDIS_RS_KEY = 'shopify-result'


def extract_email_from_url(domain: str, url: str):
    if domain.endswith('/'):
        domain = domain[: len(domain) - 1]
    spider.logger.debug("Requests before...")
    if url.startswith('http'):
        response = requests.get(url, headers=DEFAULT_REQUEST_HEADERS, timeout=(10, 10))
    else:
        response = requests.get(domain + url, headers=DEFAULT_REQUEST_HEADERS, timeout=(10, 10))
    spider.logger.debug("Requests after...")
    if response.ok:
        spider.logger.debug("EXTRACT EMAIL FROM UEL BEFORE")
        email_m = regex.search(email_rex, response.text, timeout=10)
        spider.logger.debug("EXTRACT EMAIL FROM UEL AFTER")
        if email_m and not (email_m.group(1).endswith('png') or email_m.group(1).endswith('jpg')):
            return email_m.group(1)
    return None


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


class ExtractShopifyEmail(scrapy.Spider):
    name = 'extract_shopify_email'

    def start_requests(self):
        redis = Redis(host='www.daoyang.top', port=6379, db=0)
        while redis.llen(REDIS_DS_KEY) > 0:
            spider.logger.debug("REDIS POP BEFORE")
            email = redis.lpop(REDIS_DS_KEY)
            redis.close()
            spider.logger.debug("REDIS POP AFTER")
            if email:
                yield scrapy.Request(bytes.decode(email), callback=self.parse)
                spider.logger.debug("REDIS YIELD YIELD YIELD YIELD")
            else:
                break

        # yield scrapy.Request('https://balsacircle.com/', callback=self.parse)

    def parse(self, response):
        spider.logger.debug("GET PARSE...")
        client = Redis(host='www.daoyang.top', port=6379, db=0)
        body = bytes.decode(response.body, encoding=response.encoding)

        email_m = regex.search(email_rex, body, timeout=10)
        spider.logger.debug("GET email_m...")

        facebook_m = regex.search(facebook_rex, body, timeout=10)
        spider.logger.debug("GET facebook_m...")

        twitter_m = regex.search(twitter_rex, body, timeout=10)
        spider.logger.debug("GET twitter_m...")

        instagram_m = regex.search(instagram_rex, body, timeout=10)
        spider.logger.debug("GET instagram_m...")

        email = None
        facebook = None
        twitter = None
        instagram = None

        if email_m and not (email_m.group(1).endswith('png') or email_m.group(1).endswith('jpg')):
            email = email_m.group(1)
            spider.logger.info('Find email from [main] page')
        else:
            is_find_email = False
            spider.logger.info("MATCH CONTACT_US START... " + response.url)
            contact_us = None
            try:
                contact_us = regex.search(contact_us_res, body, re.I, timeout=10)
            except TimeoutError as e:
                spider.logger.error("TIME OUT Find Contact US ", e)
            spider.logger.info("MATCH CONTACT_US AFTER...")
            if contact_us:
                spider.logger.info('Find contact from main page')
                email = extract_email_from_url(response.url, contact_us.group(1))
                if email:
                    spider.logger.info('Find email from [contact] page')
                    is_find_email = True

            if not is_find_email:
                spider.logger.info("MATCH ABOUT_US START...")
                about_us = None
                try:
                    about_us = regex.search(contact_us_res, body, re.I, timeout=10)
                except TimeoutError as e:
                    spider.logger.error("TIME OUT Find About US ", e)
                spider.logger.info("MATCH ABOUT_US AFTER...")
                if about_us:
                    spider.logger.info('Find about from main page')
                    email = extract_email_from_url(response.url, about_us.group(1))
                    if email:
                        spider.logger.info('Find email from [contact] page')

        spider.logger.debug("BEFORE FACEBOOK...")
        if facebook_m:
            facebook = facebook_m.group(1)
        if twitter_m:
            twitter = twitter_m.group(1)
        if instagram_m:
            instagram = instagram_m.group(1)

        soup = BeautifulSoup(response.body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
        text_content = u" ".join(t.strip() for t in visible_texts)

        cbk_list = [kw for kw in CBK if regex.search(kw, text_content, re.I, timeout=10)]
        bes_list = [kw for kw in BES if regex.search(kw, text_content, re.I, timeout=10)]
        beb_list = [kw for kw in BEB if regex.search(kw, text_content, re.I, timeout=10)]
        ck_list = [kw for kw in CK if regex.search(kw, text_content, re.I, timeout=10)]

        data = {
            'store': response.url,
            'email': email,
            'facebook': facebook,
            'twitter': twitter,
            'instagram': instagram,
            'cbk': cbk_list,
            'bes': bes_list,
            'beb': beb_list,
            'ck': ck_list
        }

        client.lpush(REDIS_RS_KEY, json.dumps(data))
        spider.logger.debug("REDIS LPUSH success")
        client.close()
