import os

BLACKLISTED_PROXY_PATH = "blacklisted_proxies/blacklist.txt"
WORKING_PROXY_PATH = "blacklisted_proxies/working_proxies.txt"
IMAGE_DIR = "images"
MAX_CONTEXT_WINDOW = 16000
SUMMARIZE_MODEL = "gpt-3.5-turbo-0125"
JSON_MODEL = "gpt-4o"
URL = os.environ["URL"]
MAX_WORKERS = 2
PAID_PROXY = "gw.dataimpulse.com:823"
