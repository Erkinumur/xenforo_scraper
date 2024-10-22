# Xenforo Forum Scraping Project

This project is designed to scrape forum data and posts from [Xenforo Community](https://xenforo.com/community/) using Scrapy. It allows scraping forum topics, posts, and user information.

### Create a .env File
Go to the `src` directory and create a `.env` file based on the provided .env.example. You can modify the values as needed.

```bash
cp src/.env.example src/.env
```

### Required Configuration in .env
The `.env` file must include the following mandatory parameters:

* XENFORO_USERNAME: Your Xenforo forum username.
* XENFORO_PASSWORD: Your Xenforo forum password.

[//]: # (### Optional Configuration)

[//]: # (The following environment variables are optional and have default values, but can be customized:)

[//]: # ()
[//]: # (* `SCRAPY_CONCURRENT_REQUESTS`: Number of concurrent requests made by Scrapy &#40;default: 16&#41;.)

[//]: # (* `SCRAPY_DOWNLOAD_DELAY`: Delay between requests to avoid overloading the server &#40;default: 0 )

[//]: # (  seconds&#41;.)

[//]: # (* `SCRAPY_LOG_FILE`: Path to the Scrapy log file &#40;default: log.txt&#41;.)

[//]: # (* `SCRAPY_PARSED_DATA_DIR_NAME`: Directory where the parsed data will be saved &#40;default: parsed_data&#41;.)

[//]: # ()
[//]: # (Example .env File)

[//]: # (```bash)

[//]: # (XENFORO_USERNAME=your_username)

[//]: # (XENFORO_PASSWORD=your_password)

[//]: # ()
[//]: # (SCRAPY_CONCURRENT_REQUESTS=16)

[//]: # (SCRAPY_DOWNLOAD_DELAY=0.5)

[//]: # (SCRAPY_LOG_FILE=scrapy.log)

[//]: # (SCRAPY_PARSED_DATA_DIR_NAME=parsed_data)

[//]: # (```)

## Running the Scraper

### 1. Scrape the Entire Forum
To run you need docker compose

To start scraping, run the following command:

```bash
docker compose up
```

### 2. Scrape Specific Forum

To scrape a specific forum, use the links argument followed by the URL of the forum:

```bash
FORUM_URL={forum_url} docker compose up
```

Replace {forum_url} with the actual URL of the forum you want to scrape.

### 3. Scraped Data
The scraped data is saved in `.jsonl` (JSON Lines) format in the folder specified by `SCRAPY_PARSED_DATA_DIR_NAME`, which defaults to parsed_data.

Each file will contain the parsed information such as forum topics, posts, and user data.