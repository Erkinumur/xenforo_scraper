import json

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from .items import ForumForum, ForumTopic, ForumMessage, ForumUser


class ForumPipeline:

    def open_spider(self, spider):
        # Открываем файлы для записи данных при старте паука
        self.forum_file = open(f'{spider.settings["PARSED_DATA_DIR_NAME"]}/forums.jsonl', 'w')
        self.topic_file = open(f'{spider.settings["PARSED_DATA_DIR_NAME"]}/topics.jsonl', 'w')
        self.message_file = open(f'{spider.settings["PARSED_DATA_DIR_NAME"]}/messages.jsonl', 'w')
        self.users_file = open(f'{spider.settings["PARSED_DATA_DIR_NAME"]}/users.jsonl', 'w')


    def close_spider(self, spider):
        # Закрываем файлы после завершения работы паука
        self.forum_file.close()
        self.topic_file.close()
        self.message_file.close()
        self.users_file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        line = json.dumps(adapter.asdict()) + "\n"
        # Проверяем тип элемента и сохраняем в соответствующий файл
        match item:
            case ForumForum():
                self.validate_forum(adapter, spider)
                self.forum_file.write(line)
            case ForumTopic():
                self.validate_topic(adapter, spider)
                self.topic_file.write(line)
            case ForumMessage():
                self.message_file.write(line)
            case ForumUser():
                self.users_file.write(line)
            case _:
                spider.logger.warning(f"Unknown item type: {type(item)}")

        return item

    def validate_forum(self, adapter, spider):
        if any((
                adapter["url"] in spider.settings["FORUM_IGNORE_URLS"],
                # "/categories/" in adapter["url"]
        )):
            raise DropItem(f"Ignored: {adapter['url']}")

        if any((
            not adapter["forum_id"],
            # not adapter["forum_id"].isdigit(),
        )):
            raise DropItem(f"Invalid forum_id: {adapter['url']}")

        return adapter

    def validate_topic(self, adapter, spider):
        if any((
            not adapter.get("parent_id"),
        )):
            raise DropItem(f"Have no parent_id: {adapter['url']}")