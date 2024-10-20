import json
from urllib.parse import urljoin

import scrapy
from scrapy import FormRequest, signals
from scrapy.http import Response

from src.loaders import ForumForumLoader, ForumTopicLoader, ForumMessageLoader, ForumUserLoader
from src.items import ForumForum, ForumTopic, ForumMessage, ForumUser
from src.xpaths import ForumForumXPath, ForumTopicXPath, ForumMessageXPath, ForumUserXPath, \
    ForumLoginXPath


class XenforoSpider(scrapy.Spider):
    name = "xenforo"
    allowed_domains = ["xenforo.com"]
    start_urls = ["https://xenforo.com/community/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_to_parse = set()
        self.logged_in = False

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(XenforoSpider, cls).from_crawler(crawler, *args, **kwargs)

        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)

        return spider

    def parse(self, response: Response, **kwargs):
        self.log("Settings: " + str(self.settings.attributes))
        arg_links = getattr(self, 'links', None)
        if arg_links:
            forum_links = arg_links.split(',')
        else:
            forum_links = response.xpath(ForumForumXPath.LINKS)

        yield from response.follow_all(forum_links, self.parse_forum, meta={"first_page": True})

    def parse_forum(self, response: Response, **kwargs):

        first_page = response.meta.get("first_page", True)
        forum_id = None

        if first_page:
            il = ForumForumLoader(ForumForum(), selector=response, response=response)

            il.add_value('url', response.url)
            il.add_xpath('name', ForumForumXPath.NAME)
            il.add_xpath('description', ForumForumXPath.DESCRIPTION)
            il.add_value('forum_id', response.xpath(ForumForumXPath.FORUM_ID).get())
            il.add_value('parent_id', response.meta.get('parent_id', None))

            item = il.load_item()

            forum_id = item['forum_id']

            yield item

            nested_forum_links = response.xpath(ForumForumXPath.LINKS)

            if nested_forum_links:
                yield from response.follow_all(nested_forum_links, self.parse_forum,
                                               meta={"first_page": True, "parent_id": forum_id}, )

        if not forum_id:
            forum_id = response.meta.get('forum_id', "")

        topic_links = response.xpath(ForumTopicXPath.LINKS)

        if topic_links:
            yield from response.follow_all(topic_links, self.parse_topic,
                                           meta={'forum_id': forum_id}, )

        next_page = response.xpath(ForumTopicXPath.NEXT_PAGE).get()

        if next_page:
            yield response.follow(
                next_page,
                self.parse_forum,
                meta={"first_page": False, 'forum_id': forum_id},
            )

    def parse_topic(self, response: Response, **kwargs):
        forum_id = response.meta.get('forum_id', "")

        il = ForumTopicLoader(ForumTopic(), selector=response, response=response)

        il.add_value('url', response.url)
        il.add_xpath('name', ForumTopicXPath.TITLE)
        il.add_xpath('description', ForumTopicXPath.DESCRIPTION)
        il.add_value('topic_id', response.xpath(ForumTopicXPath.TOPIC_ID).get())
        il.add_value('parent_id', forum_id)
        il.add_xpath('creator_id', ForumTopicXPath.CREATOR_ID)

        item = il.load_item()

        self.users_to_parse.add(
            urljoin(
                self.settings['XENFORO_BASE_URL'],
                response.xpath(ForumTopicXPath.CREATOR_URL).get()
            )
        )
        self.log(f"Added user: {item['creator_id']} | Topic: {item['topic_id']} | {response.xpath(ForumTopicXPath.CREATOR_URL).get()}")

        yield item

        response.meta['topic_id'] = item['topic_id']

        yield from self.parse_message(response, **kwargs)

    def parse_message(self, response: Response, **kwargs):
        topic_id = response.meta['topic_id']
        articles = response.xpath(ForumMessageXPath.ARTICLES)

        for article in articles:
            il = ForumMessageLoader(ForumMessage(), selector=article, response=response)

            il.add_value('message_id', article.attrib[ForumMessageXPath.MESSAGE_ID_ATTRIB_NAME])
            il.add_value('message_timestamp', response.xpath(ForumMessageXPath.CREATED_AT).get())
            il.add_xpath('url', ForumMessageXPath.URL)
            il.add_xpath('message', ForumMessageXPath.MESSAGE_BODY)
            il.add_value('topic_id', topic_id)
            il.add_xpath('user_id', ForumMessageXPath.CREATOR_ID)

            item = il.load_item()

            self.users_to_parse.add(
                urljoin(
                    self.settings['XENFORO_BASE_URL'],
                    article.xpath(ForumMessageXPath.CREATOR_URL).get()
                )
            )
            self.log(f"Added user: {item['user_id']} | Message: {item['message_id']} |"
                     f" {article.xpath(ForumMessageXPath.CREATOR_URL).get()} | "
                     f"{                urljoin(
                    self.settings['XENFORO_BASE_URL'],
                    article.xpath(ForumMessageXPath.CREATOR_URL).get()
                )}")

            yield item

        next_page = response.xpath(ForumMessageXPath.NEXT_PAGE).get()

        if next_page:
            yield response.follow(
                next_page,
                self.parse_message,
                meta={'topic_id': topic_id},
            )

    def login(self, response: Response, **kwargs):
        xf_token = response.xpath(ForumLoginXPath.XF_TOKEN).get()

        yield FormRequest(
            url="https://xenforo.com/community/login/login",
            formdata={
                "login": self.settings['XENFORO_USERNAME'],
                "password": self.settings['XENFORO_PASSWORD'],
                "_xfToken": xf_token,
                "remember": "1",
                "_xfRedirect": "https://xenforo.com/community/",
            },
            callback=self.after_login,
        )

    def after_login(self, response: Response):
        self.logged_in = True

        self.log("Successfully logged in. Starting to scrape users.")

        for url in self.users_to_parse:
            yield response.follow(url, callback=self.parse_user)

    def parse_user(self, response: Response, **kwargs):
        user_data = {
            'url': response.url,
            'login': response.xpath(ForumUserXPath.LOGIN).get(),
            'user_id': response.xpath(ForumUserXPath.USER_ID).get(),
            'avatar': response.xpath(ForumUserXPath.AVATAR).get(),
            'registration_date': response.xpath(ForumUserXPath.REGISTRATION_DATE).get(),
            'last_visit_date': response.xpath(ForumUserXPath.LAST_VISIT_DATE).get(),
            'signature': response.xpath(ForumUserXPath.SIGNATURE).get(),
            'bio': response.xpath(ForumUserXPath.BIO).get(),
        }

        xf_token = response.xpath(ForumLoginXPath.XF_TOKEN).get()
        params = {
            "_xfResponseType": "html",
            "_xfWithData": 1,
            "_xfRequestUri": user_data["url"],
            "_xfToken": xf_token,
        }
        params_str = '&'.join([f'{k}={v}' for k, v in params.items()])
        url = f'{user_data["url"]}about/?{params_str}'

        yield response.follow(url, callback=self.parse_user_about, meta={'user_data': user_data})

    def parse_user_about(self, response: Response, **kwargs):
        user_data = response.meta['user_data']

        il = ForumUserLoader(ForumUser(), selector=response, response=response)

        il.add_value('url', user_data['url'])
        il.add_value('login', user_data['login'])
        il.add_value('user_id', user_data['user_id'])
        il.add_value('avatar', user_data['avatar'])
        il.add_value('registration_date', user_data['registration_date'])
        il.add_value('last_visit_date', user_data['last_visit_date'])
        il.add_value('signature', user_data['signature'])
        il.add_value('bio', user_data['bio'])

        other_info_data = response.xpath(ForumUserXPath.OTHER_INFO)
        other_info = {}
        for data in other_info_data:
            values = data.xpath('dd//text()').getall()
            value = ' '.join(filter(lambda x: x.strip(), values)).strip()
            other_info[data.xpath('dt/text()').get().lower()] = value

        il.add_value('website', other_info.get('website'))
        il.add_value('birthdate', other_info.get('birthday'))
        il.add_value('discord', other_info.get('discord'))
        il.add_value('email', other_info.get('email'))
        il.add_value('phone_number', other_info.get('phone'))
        il.add_value('telegram', other_info.get('telegram_user'))
        il.add_value('other_json_user_information', json.dumps(other_info))

        item = il.load_item()

        yield item

    def spider_idle(self, spider):

        self.log("Spider idle.")
        if not self.logged_in and self.users_to_parse:
            self.log("Logging in to scrape users.")
            self.crawler.engine.crawl(
                scrapy.Request("https://xenforo.com/community/login", callback=self.login)
            )
        else:
            self.log("No users to scrape or already logged in.")
