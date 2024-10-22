import re
from datetime import datetime
from urllib.parse import urljoin

from w3lib.html import remove_tags

from .settings import XENFORO_BASE_URL
from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Compose


def clean_id(value):
    data = value.split('-')

    try:
        id_ =  int(data[-1])
    except ValueError:
        return None

    if data[0] == 'category':
        return 9_000_000 + id_

    return id_


def join_urls(value):
    return urljoin(XENFORO_BASE_URL, value)


def format_birthday(value):
    date_str = re.sub(r"\(.*\)", "", value).strip()

    if not date_str:
        return None

    try:
        return datetime.strptime(date_str, "%b %d, %Y")
    except ValueError:
        pass

    try:
        return datetime.strptime(f"{date_str} 1804", "%B %d %Y")
    except ValueError:
        pass

    return None

class ForumForumLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    forum_id_in = MapCompose(clean_id)
    parent_id_in = MapCompose(int)
    creator_id_in = MapCompose(int)


class ForumTopicLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    topic_id_in = MapCompose(clean_id)
    parent_id_in = MapCompose(int)
    creator_id_in = MapCompose(int)


class ForumMessageLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    message_id_in = MapCompose(clean_id)
    url_in = MapCompose(str.strip, join_urls)
    message_in = MapCompose(remove_tags, str.strip)
    message_timestamp_in = MapCompose(datetime.fromisoformat)
    message_timestamp_out = Compose(MapCompose(datetime.timestamp), TakeFirst())
    topic_id_in = MapCompose(int)
    user_id_in = MapCompose(int)


class ForumUserLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    user_id_in = MapCompose(int)
    avatar_in = MapCompose(str.strip, join_urls)
    # registration_date_in = MapCompose(datetime.fromisoformat)
    # last_visit_date_in = MapCompose(datetime.fromisoformat)
    signature_in = MapCompose(remove_tags, str.strip)
    bio_in = MapCompose(remove_tags, str.strip)
    birthdate_in = MapCompose(format_birthday)
    birthdate_out = Compose(MapCompose(lambda x: x.strftime("%Y-%m-%d")), TakeFirst())