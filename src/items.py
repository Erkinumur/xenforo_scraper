# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ForumUser(scrapy.Item):
    login = scrapy.Field()
    last_name = scrapy.Field()
    first_name = scrapy.Field()
    display_name = scrapy.Field()  #
    user_id = scrapy.Field()  #
    avatar = scrapy.Field()  #
    url = scrapy.Field()
    status = scrapy.Field()  #
    signature = scrapy.Field()

    jabber = scrapy.Field()
    aim = scrapy.Field()
    email = scrapy.Field()
    phone_number = scrapy.Field()
    icq = scrapy.Field()
    birthdate = scrapy.Field()
    registration_date = scrapy.Field()
    last_visit_date = scrapy.Field()
    bio = scrapy.Field()
    website = scrapy.Field()
    ip = scrapy.Field()
    discord = scrapy.Field()
    telegram_user = scrapy.Field()
    other_json_user_information = scrapy.Field()  #


class ForumForum(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    creator_id = scrapy.Field()
    forum_id = scrapy.Field()
    parent_id = scrapy.Field()
    url = scrapy.Field()


class ForumTopic(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    creator_id = scrapy.Field()
    topic_id = scrapy.Field()
    parent_id = scrapy.Field()
    url = scrapy.Field()


class ForumMessage(scrapy.Item):
    message = scrapy.Field()
    url = scrapy.Field()
    message_id = scrapy.Field()
    message_timestamp = scrapy.Field()
    topic_id = scrapy.Field()

    user_id = scrapy.Field()


class ForumQuote(scrapy.Item):
    message_id = scrapy.Field()
    quoted_message_id = scrapy.Field()
    quote_text = scrapy.Field()