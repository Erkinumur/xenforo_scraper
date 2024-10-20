# Xenforo Forum Scraping Project

This project is designed to scrape forum data and posts from [Xenforo Community](https://xenforo.com/community/) using Scrapy. It allows scraping forum topics, posts, and user information.

## Setup Instructions

### 1. Install Dependencies
Make sure you have pip and virtualenv installed. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 2. Create a .env File
Go to the src directory and create a .env file based on the provided .env.example. You can modify the values as needed.

```bash
cp src/.env.example src/.env
```

### 3. Required Configuration in .env
The `.env` file must include the following mandatory parameters:

* XENFORO_USERNAME: Your Xenforo forum username.
* XENFORO_PASSWORD: Your Xenforo forum password.

### 4. Optional Configuration
The following environment variables are optional and have default values, but can be customized:

* `SCRAPY_CONCURRENT_REQUESTS`: Number of concurrent requests made by Scrapy (default: 16).
* `SCRAPY_DOWNLOAD_DELAY`: Delay between requests to avoid overloading the server (default: 0 
  seconds).
* `SCRAPY_LOG_FILE`: Path to the Scrapy log file (default: log.txt).
* `SCRAPY_PARSED_DATA_DIR_NAME`: Directory where the parsed data will be saved (default: parsed_data).

Example .env File
```bash
XENFORO_USERNAME=your_username
XENFORO_PASSWORD=your_password

SCRAPY_CONCURRENT_REQUESTS=16
SCRAPY_DOWNLOAD_DELAY=0.5
SCRAPY_LOG_FILE=scrapy.log
SCRAPY_PARSED_DATA_DIR_NAME=parsed_data
```

## Running the Spider

### 1. Scrape the Entire Forum

To start scraping the forum, run the following command:

```bash
scrapy crawl xenforo
```

### 2. Scrape Specific Forum

To scrape a specific forum, use the links argument followed by the URL of the forum:

```bash
scrapy crawl xenforo -a links={forum_url}
```

Replace {forum_url} with the actual URL of the forum you want to scrape.

### 3. Scraped Data
The scraped data is saved in `.jsonl` (JSON Lines) format in the folder specified by `SCRAPY_PARSED_DATA_DIR_NAME`, which defaults to parsed_data.

Each file will contain the parsed information such as forum topics, posts, and user data.