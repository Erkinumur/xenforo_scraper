class ForumForumXPath:
    LINKS = ('//a[@data-xf-init="element-tooltip" '
             'and not(contains(@href, "help")) '
             'and not(contains(@href, "threads"))]')
    NAME = '//h1[@class="p-title-value"]/text()'
    DESCRIPTION = '//div[@class="p-description"]/text()'
    FORUM_ID = '//@data-content-key'


class ForumTopicXPath:
    LINKS = '//a[@data-preview-url]'
    NEXT_PAGE = '//a[@class="pageNav-jump pageNav-jump--next"]/@href'
    TITLE = '//h1/text()'
    DESCRIPTION = '//meta[@name="description"]/@content'
    TOPIC_ID = '//@data-content-key'
    CREATOR_ID = '//a[@class="username  u-concealed"]/@data-user-id'
    CREATOR_URL = '//a[@class="username  u-concealed"]/@href'
    MESSAGE = '//div[@class="message-inner"]/p/text()'


class ForumMessageXPath:
    ARTICLES = '//article[@data-content]'
    MESSAGE_ID_ATTRIB_NAME = 'data-content'
    CREATOR_ID = './/a[@data-user-id]/@data-user-id'
    CREATOR_URL = './/a[@data-user-id]/@href'
    CREATED_AT = './/time/@datetime'
    URL = './/a[@aria-label="Share"]/@href'
    MESSAGE_BODY = './/article[contains(@class, "message-body")]'
    NEXT_PAGE = '//a[@class="pageNav-jump pageNav-jump--next"]/@href'


class ForumUserXPath:
    LOGIN = '//span[@class="username "]//text()'
    USER_ID = '//span[@class="username "]/@data-user-id'
    AVATAR = '//span[@class="memberHeader-avatar"]//img[contains(@class, "avatar")]/@src'
    REGISTRATION_DATE = '//dt[text()="Joined"]/..//time/@datetime'
    LAST_VISIT_DATE = '//dt[text()="Last seen"]/..//time/@datetime'
    SIGNATURE = '//h4[text()="Signature"]/../div'
    BIO = '//li[@aria-labelledby="about"]//div[@class="block-body"]/div[1]/div[@class="bbWrapper"]'
    OTHER_INFO = '//div[@class="block-body"]//dl'


class ForumLoginXPath:
    XF_TOKEN = '//input[@name="_xfToken"]/@value'