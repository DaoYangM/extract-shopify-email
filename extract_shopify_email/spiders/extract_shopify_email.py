import csv
import json
import re

import requests
import scrapy
from redis import StrictRedis
from scrapy.utils import spider

contact_us_res = r"""<a.*?href="(.*?)".*?>contact.*?</a>"""
about_us_res = r"""<a.*?href="(.*?)".*?>about.*?</a>"""
email_rex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
facebook_rex = r'href="(https://www.facebook.com/.*?)"'
twitter_rex = r'href="(https://(www.)?twitter.com/.*?)"'
instagram_rex = r'href="(https://www.instagram.com/.*?)"'


def extract_email_from_url(domain: str, url: str):
    if domain.endswith('/'):
        domain = domain[: len(domain) - 1]
    if url.startswith('http'):
        url = url.replace(domain, '')
    response = requests.get(domain + url)
    if response.ok:
        email_m = re.search(email_rex, response.text)
        if email_m and not (email_m.group(1).endswith('png') or email_m.group(1).endswith('jpg')):
            return email_m.group(1)
    return None


class ExtractShopifyEmail(scrapy.Spider):
    name = 'extract_shopify_email'
    REDIS_DS_KEY = 'shopify-email'
    REDIS_RS_KEY = 'shopify-result'
    redis = StrictRedis(host='www.daoyang.top', port=6379, db=0)

    def start_requests(self):

        while True:
            email = self.redis.lpop(self.REDIS_DS_KEY)
            if email:
                yield scrapy.Request(bytes.decode(email), callback=self.parse)
            else:
                break

    def parse(self, response):
        body = bytes.decode(response.body)

        email_m = re.search(email_rex, body)
        facebook_m = re.search(facebook_rex, body)
        twitter_m = re.search(twitter_rex, body)
        instagram_m = re.search(instagram_rex, body)

        email = None
        facebook = None
        twitter = None
        instagram = None

        if email_m and not (email_m.group(1).endswith('png') or email_m.group(1).endswith('jpg')):
            email = email_m.group(1)
            spider.logger.info('find email from [main] page')
        else:
            is_find_email = False
            contact_us = re.search(contact_us_res, body, re.I)
            if contact_us:
                spider.logger.info('find contact from main page')
                email = extract_email_from_url(response.url, contact_us.group(1))
                if email:
                    spider.logger.info('find email from [contact] page')
                    is_find_email = True

            if not is_find_email:
                about_us = re.search(about_us_res, body, re.I)
                if about_us:
                    spider.logger.info('find about from main page')
                    email = extract_email_from_url(response.url, about_us.group(1))
                    if email:
                        spider.logger.info('find email from [contact] page')

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

        self.redis.lpush(self.REDIS_RS_KEY, json.dumps(data))