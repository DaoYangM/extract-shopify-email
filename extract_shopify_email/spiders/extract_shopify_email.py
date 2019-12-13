import json
import re

import regex
import requests
import scrapy
from redis import Redis
from scrapy.utils import spider

from extract_shopify_email.settings import DEFAULT_REQUEST_HEADERS

contact_us_res = r'<a .*?href="(.*?)" .*?>contact us</a>'
about_us_res = r'<a .*?href="(.*?)" .*?>about us</a>'
email_rex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
facebook_rex = r'href="(https://www.facebook.com/.*?)"'
twitter_rex = r'href="(https://(www.)?twitter.com/.*?)"'
instagram_rex = r'href="(https://www.instagram.com/.*?)"'

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
        email_m = email_rex.search(response.text)
        spider.logger.debug("EXTRACT EMAIL FROM UEL AFTER")
        if email_m and not (email_m.group(1).endswith('png') or email_m.group(1).endswith('jpg')):
            return email_m.group(1)
    return None


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
            contact_us = regex.search(contact_us_res, body, re.I, timeout=10)
            spider.logger.info("MATCH CONTACT_US AFTER...")
            if contact_us:
                spider.logger.info('Find contact from main page')
                email = extract_email_from_url(response.url, contact_us.group(1))
                if email:
                    spider.logger.info('Find email from [contact] page')
                    is_find_email = True

            if not is_find_email:
                spider.logger.info("MATCH ABOUT_US START...")
                about_us = regex.search(contact_us_res, body, re.I, timeout=10)
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

        data = {
            'store': response.url,
            'email': email,
            'facebook': facebook,
            'twitter': twitter,
            'instagram': instagram

        }

        client.lpush(REDIS_RS_KEY, json.dumps(data))
        spider.logger.debug("REDIS LPUSH success")
        client.close()
