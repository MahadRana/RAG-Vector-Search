import requests                     
from bs4 import BeautifulSoup
import sys
from src.exception import CustomException
from src.logger import logging

def load_html_page(url:str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/116.0.0.0 Safari/537.36",
        }
        logging.info(f"load_html_page: fetching URL: {url}")
        response = requests.get(url, headers=headers)
        logging.debug(f"load_html_page: got response {response.status_code} for {url}")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        main = soup.find("div", class_='main_content') or soup
        paragraphs = main.find_all("p")
        logging.info(f"load_html_page: extracted {len(paragraphs)} <p> tags from {url}")
        return "\n\n".join(p.get_text(strip=True) for p in paragraphs)
    except Exception as e:
        logging.error(f"load_html_page: error fetching {url}: {e}", exc_info=True)
        raise CustomException(e,sys)
    