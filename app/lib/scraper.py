import requests
from bs4 import BeautifulSoup

def scrape_prices(search_query):
    base_url = "https://listado.mercadolibre.com.ec/"
    url = f"{base_url}{search_query.replace(' ', '-')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return []  # Retorna una lista vacía si hay un error en la solicitud
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    products = []
    
    # Buscar los productos en la página
    for item in soup.find_all("li", class_="ui-search-layout__item"):
        try:
            name = item.find("h2", class_="ui-search-item__title").text.strip()
            price = item.find("span", class_="price-tag-fraction").text.strip()
            link = item.find("a", class_="ui-search-link")["href"]
            products.append({"Name": name, "Price": price, "Link": link})
        except AttributeError:
            continue  # Si falta algún dato, continuar con el siguiente producto
    
    return products