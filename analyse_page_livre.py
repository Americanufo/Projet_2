import requests
import re
from bs4 import BeautifulSoup

# Extraction de la page HTML avec requests
response = requests.get("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")

# Extraction des informations souhaitées avec Beautiful Soup
soup = BeautifulSoup(response.content, "html.parser")
  
# Extraction de l'url de la page du livre avec requests
product_page_url = response.url 
print(f"URL de la page du livre : {product_page_url}")

# Extraire le titre du livre dans la page HTML  
title = soup.find("h1").text
print(f"Titre : {title}")

# Extraction de l'UPC (Universal Product Code) 
universal_product_code = soup.find('th', string='UPC')  
universal_product_code = universal_product_code.find_next('td').text
print(f"UPC : {universal_product_code}")


# Extraction du prix TTC 
price_including_tax = soup.find("th", string="Price (incl. tax)") 
price_including_tax = price_including_tax.find_next("td").text
# Supprime les caractères non numériques
price_including_tax = re.sub(r"[^\d.]", "", price_including_tax)
print(f"Price (incl. tax) : {price_including_tax}")

# Extraction du prix HT 
price_excluding_tax = soup.find("th", string="Price (excl. tax)") 
price_excluding_tax = price_excluding_tax.find_next("td").text
# Supprime les caractères non numériques
price_excluding_tax = re.sub(r"[^\d.]", "", price_excluding_tax)
print(f"Price (excl. tax): {price_excluding_tax}")

# Extraction du nombre d'exemplaires disponibles
number_available = soup.find("th", string="Availability")
number_available = number_available.find_next("td").text
# Supprime les caractères non numériques
number_available = re.sub(r"[^\d]", "", number_available)
print(f"Number available : {number_available}")

# Extraction de la description du livre
product_description = soup.find("h2", string="Product Description")
product_description = product_description.find_next("p").text
print(f"Product description : {product_description}")

# Extraction de la catégorie du livre   
breadcrumb_links = soup.find_all('a')
category = breadcrumb_links[-1].text
print(f"Category : {category}")

# Extraction de la note du livre
star_rating = soup.find('p', class_='star-rating')
rating_class = star_rating.get('class')
if rating_class:
    rating = rating_class[1]  
    star_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    review_rating = star_map.get(rating, 0)
    print(f"Nombre d'étoiles : {review_rating}")

# Extraction de l'url de l'image du livre
image_url = soup.find("img")["src"] 
from urllib.parse import urljoin
image_url = urljoin(response.url, image_url)
print(f"URL de l'image : {image_url}")


# Extraire les informations dans un fichier CSV pour chaque catégorie
import csv
write_csv = open("informations_livre.csv", "w", newline="")
csv_writer = csv.writer(write_csv)  
csv_writer.writerow(["product_page_url", "title", "universal_product_code", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"])
csv_writer.writerow([product_page_url, title, universal_product_code, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
write_csv.close()
