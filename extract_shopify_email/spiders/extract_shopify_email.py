import json
import re

import requests
import scrapy
from redis import Redis
from scrapy.utils import spider

from extract_shopify_email.settings import DEFAULT_REQUEST_HEADERS

contact_us_res = r"""<a.*?href="(.*?)".*?>contact.*?</a>"""
about_us_res = r"""<a.*?href="(.*?)".*?>about.*?</a>"""
email_rex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
facebook_rex = r'href="(https://www.facebook.com/.*?)"'
twitter_rex = r'href="(https://(www.)?twitter.com/.*?)"'
instagram_rex = r'href="(https://www.instagram.com/.*?)"'

REDIS_DS_KEY = 'shopify-email'
REDIS_RS_KEY = 'shopify-result'


def extract_email_from_url(domain: str, url: str):
    if domain.endswith('/'):
        domain = domain[: len(domain) - 1]
    spider.logger.info("Requests before...")
    if url.startswith('http'):
        response = requests.get(url, headers=DEFAULT_REQUEST_HEADERS, timeout=(10, 10))
    else:
        response = requests.get(domain + url, headers=DEFAULT_REQUEST_HEADERS, timeout=(10, 10))
    spider.logger.info("Requests after...")
    if response.ok:
        spider.logger.info("EXTRACT EMAIL FROM UEL BEFORE")
        email_m = re.search(email_rex, response.text)
        spider.logger.info("EXTRACT EMAIL FROM UEL AFTER")
        if email_m and not (email_m.group(1).endswith('png') or email_m.group(1).endswith('jpg')):
            return email_m.group(1)
    return None


class ExtractShopifyEmail(scrapy.Spider):
    name = 'extract_shopify_email'

    def start_requests(self):
        redis = Redis(host='124.156.206.235', port=6379, db=0)
        while redis.llen(REDIS_DS_KEY) > 0:
            spider.logger.info("REDIS POP BEFORE")
            email = redis.lpop(REDIS_DS_KEY)
            redis.close()
            spider.logger.info("REDIS POP AFTER")
            if email:
                yield scrapy.Request(bytes.decode(email), callback=self.parse)
                spider.logger.info("REDIS YIELD YIELD YIELD YIELD")
            else:
                break

        # yield scrapy.Request('https://balsacircle.com/', callback=self.parse)

    def parse(self, response):
        spider.logger.info("GET PARSE...")
        client = Redis(host='124.156.206.235', port=6379, db=0)
        body = bytes.decode(response.body, encoding=response.encoding)

        email_m = re.search(email_rex, body)
        spider.logger.info("GET email_m...")

        facebook_m = re.search(facebook_rex, body)
        spider.logger.info("GET facebook_m...")

        twitter_m = re.search(twitter_rex, body)
        spider.logger.info("GET twitter_m...")

        instagram_m = re.search(instagram_rex, body)
        spider.logger.info("GET instagram_m...")

        email = None
        facebook = None
        twitter = None
        instagram = None

        if email_m and not (email_m.group(1).endswith('png') or email_m.group(1).endswith('jpg')):
            email = email_m.group(1)
            spider.logger.info('Find email from [main] page')
        else:
            is_find_email = False
            contact_us = re.search(contact_us_res, body, re.I)
            if contact_us:
                spider.logger.info('Find contact from main page')
                email = extract_email_from_url(response.url, contact_us.group(1))
                if email:
                    spider.logger.info('Find email from [contact] page')
                    is_find_email = True

            if not is_find_email:
                about_us = re.search(about_us_res, body, re.I)
                if about_us:
                    spider.logger.info('Find about from main page')
                    email = extract_email_from_url(response.url, about_us.group(1))
                    if email:
                        spider.logger.info('Find email from [contact] page')

        spider.logger.info("BEFORE FACEBOOK...")
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
        spider.logger.info("REDIS LPUSH success")
        client.close()
