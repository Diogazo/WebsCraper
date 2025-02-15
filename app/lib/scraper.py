import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_prices(search_query):
    base_url = "https://listado.mercadolibre.com.ec/"
    url = f"{base_url}{search_query.replace(' ', '-')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    products = []
    
    for item in soup.find_all("div", class_="ui-search-result__content-wrapper"):
        try:
            name = item.find("h2", class_="ui-search-item__title").text
            price = item.find("span", class_="price-tag-fraction").text
            link = item.find("a", class_="ui-search-link")["href"]
            products.append({"Name": name, "Price": price, "Link": link})
        except AttributeError:
            continue
    
    return products

def scrape_prices(search):
    # Simulación de datos de scraping
    return [
        {"Name": "Producto 1", "Price": "$100", "Link": "https://listado.mercadolibre.com.ec/accesorios-vehiculos/acc-motos-cuatrimotos/"},
        {"Name": "Producto 2", "Price": "$200", "Link": "https://www.mercadolibre.com.ec/c/computacion#menu=categories"},
    ]
