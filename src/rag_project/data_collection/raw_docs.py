import requests                     
from bs4 import BeautifulSoup
from typing import List    

def load_html_page(url:str) -> str:
    response = response.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html-parser')
    main = soup.find("div", class_='main_content') or soup
    paragraphs = main.find_all("p")
    return "\n\n".join(p.get_text(strip=True) for p in paragraphs)

def load_all_pages(url_lst:List) -> List:
    raw_docs = []
    for url in url_lst:
        text = load_html_page(url)
        raw_docs.append({
            "id": url,           
            "text": text,
            "metadata": {"source": url},
        })
    