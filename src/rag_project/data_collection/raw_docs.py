import requests                     
from bs4 import BeautifulSoup
from typing import List    
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
    

def load_all_pages(url_lst:List) -> List:
    logging.info(f"load_all_pages: Retriving text from {len(url_lst)} pages")
    raw_docs = []
    for idx, url in enumerate(url_lst):
        logging.info(f"load_all_pages: loading page {idx+1}/{len(url_lst)}: {url}")
        text = load_html_page(url)
        raw_docs.append({
            "id": url,           
            "text": text,
            "metadata": {"source": url},
        })
    logging.info("load_all_pages: pages loaded successfully!")
    return raw_docs
    