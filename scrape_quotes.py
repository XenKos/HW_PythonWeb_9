import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def scrape_quotes():
    quotes = []
    authors = {}
    page = 1
    while True:
        soup = get_soup(f"{BASE_URL}/page/{page}/")
        quote_elements = soup.select('.quote')
        if not quote_elements:
            break
        
        for quote_element in quote_elements:
            text = quote_element.select_one('.text').get_text()
            author = quote_element.select_one('.author').get_text()
            tags = [tag.get_text() for tag in quote_element.select('.tag')]
            
            if author not in authors:
                author_url = BASE_URL + quote_element.select_one('span a')['href']
                author_soup = get_soup(author_url)
                born_date = author_soup.select_one('.author-born-date').get_text()
                born_location = author_soup.select_one('.author-born-location').get_text()
                description = author_soup.select_one('.author-description').get_text()
                
                authors[author] = {
                    'fullname': author,
                    'born_date': born_date,
                    'born_location': born_location,
                    'description': description
                }
            
            quotes.append({
                'quote': text,
                'author': author,
                'tags': tags
            })
        
        page += 1
    
    return quotes, list(authors.values())

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    quotes, authors = scrape_quotes()
    save_to_json(quotes, 'quotes.json')
    save_to_json(authors, 'authors.json')

if __name__ == "__main__":
    main()