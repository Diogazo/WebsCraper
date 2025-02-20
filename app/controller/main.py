import sys
import os

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.lib.scraper import scrape_prices
from app.model.database import Database

def main(search_query):
    products = scrape_prices(search_query)
    
    db = Database()
    for product in products:
        db.insert(product)
    
    # Generar una página HTML con los productos
    html_content = "<html><body><h1>Productos</h1><ul>"
    for product in products:
        html_content += f'<li><a href="{product["Link"]}">{product["Name"]} - {product["Price"]}</a></li>'
    html_content += "</ul></body></html>"
    
    # Guardar el contenido HTML en un archivo
    with open("productos.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    
    print("Archivo HTML generado: productos.html")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        search_query = sys.argv[1]
        main(search_query)
    else:
        print("Por favor, proporciona un término de búsqueda.")