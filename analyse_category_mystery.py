import requests
import re
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Extraction de la page HTML avec requests
response = requests.get("http://books.toscrape.com/catalogue/category/books/mystery_3/index.html")

# Extraction des informations souhaitées avec Beautiful Soup
soup = BeautifulSoup(response.content, "html.parser")

# Créer un fichier CSV pour stocker les informations des livres
fieldnames = [
    "product_page_url",
    "title",
    "UPC",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"
]

# Ouvrir le fichier CSV en mode écriture pour ajouter l'en-tête
with open("category_mystery.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# Extraction des url des livres de la catégorie Mystery
books_url = soup.find_all("h3")
product_page_url = []
for url in books_url:
    product_page_url.append("http://books.toscrape.com/catalogue" + url.a["href"][8:])
    
# Vérification de la page suivante et ajout de ses livres
if next_page := soup.find("li", class_="next"):
    next_page = next_page.a["href"]
    response = requests.get("http://books.toscrape.com/catalogue/category/books/mystery_3/" + next_page)
    soup = BeautifulSoup(response.content, "html.parser")
    books_url = soup.find_all("h3")
    for url in books_url:
        product_page_url.append("http://books.toscrape.com/catalogue" + url.a["href"][8:])
print(f"URL des pages des livres : {product_page_url}")

# Extraire les informations des livres de la catégorie Mystery
for url in product_page_url:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extraction de l'url de la page du livre avec requests
    book_url = response.url
    print(f"URL de la page du livre : {book_url}")
    
    # Extraire le titre du livre dans la page HTML  
    title = soup.find("h1").text.strip()
    print(f"Titre : {title}")
    
    # Extraction de l'UPC (Universal Product Code) 
    universal_product_code = soup.find('th', string='UPC')  
    universal_product_code = universal_product_code.find_next('td').text
    print(f"UPC : {universal_product_code}")
    
    # Extraction du prix TTC 
    price_including_tax = soup.find("th", string="Price (incl. tax)") 
    price_including_tax = price_including_tax.find_next("td").text
    # Supprime les caractères non numérique
    price_including_tax = re.sub(r"[^\d.]", "", price_including_tax)
    print(f"Prix (TTC) : {price_including_tax}")
    
    # Extraction du prix HT 
    price_excluding_tax = soup.find("th", string="Price (excl. tax)") 
    price_excluding_tax = price_excluding_tax.find_next("td").text
    # Supprime les caractères non numérique
    price_excluding_tax = re.sub(r"[^\d.]", "", price_excluding_tax)
    print(f"Prix (Hors taxe): {price_excluding_tax}")
    
    # Extraction du nombre d'exemplaires disponibles
    number_available = soup.find("th", string="Availability")
    number_available = number_available.find_next("td").text
    # Supprime les caractères non numérique
    number_available = re.sub(r"[^\d]", "", number_available)
    print(f"Nombre d'exemplaire disponible : {number_available}")
    
    # Extraction de la description du livre
    product_description = soup.find("h2", string="Product Description")
    product_description = product_description.find_next("p").text if product_description else "No description"
    print(f"Description : {product_description}")
    
    # Extraction de la catégorie du livre   
    breadcrumb_links = soup.find_all('a')
    category = breadcrumb_links[3].text if len(breadcrumb_links) > 3 else "Unknown"
    print(f"Categorie : {category}")

    # Extraction de la note du livre
    star_rating = soup.find('p', class_='star-rating')
    rating_class = star_rating.get('class') if star_rating else []
    review_rating = 0  # Valeur par défaut si aucune note n'est trouvée
    if rating_class:
        rating = rating_class[1]  
        star_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        review_rating = star_map.get(rating, 0)
    print(f"Nombre d'étoiles : {review_rating}")
    
    # Extraction de l'url de l'image du livre
    image_url = soup.find("img")["src"]
    image_url = urljoin(response.url, image_url)
    print(f"URL de l'image : {image_url}")

    # Écrire les informations dans le fichier CSV
    with open("category_mystery.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            "product_page_url": book_url,
            "title": title,
            "UPC": universal_product_code,
            "price_including_tax": price_including_tax,
            "price_excluding_tax": price_excluding_tax,
            "number_available": number_available,
            "product_description": product_description,
            "category": category,
            "review_rating": review_rating,
            "image_url": image_url
        })

    print("\n")

print("Extraction des informations terminée !")