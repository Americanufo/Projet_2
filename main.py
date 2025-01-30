import requests
import re
import csv
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Extraction de la page HTML avec requests
response = requests.get("https://books.toscrape.com/")

# Extraction des informations souhaitées avec Beautiful Soup
soup = BeautifulSoup(response.content, "html.parser")

# Chercher les catégories sur le site
categories = soup.find("ul", class_="nav-list")
categories = categories.find_all("a")
category_id = {}

# Extraire les catégories et leurs identifiants
for category in categories:
    category_name = category.text.strip()
    category_url = category["href"]
    category_id[category_name] = int(re.search(r"\d+", category_url).group())


# En-têtes pour les fichiers CSV
fieldnames = [
    "product_page_url", "title", "UPC", "price_including_tax", "price_excluding_tax", 
    "number_available", "product_description", "category", "review_rating", "image_url","image_path"
]

# Créer un dossier pour les catégories et les images
os.makedirs("categories", exist_ok=True)
os.makedirs("images", exist_ok=True)


# Ouvrir le fichier CSV en mode écriture pour chaque catégorie dans le dossier nommé "categories"
for category, category_id in category_id.items():
    csv_filename = f"category_{category}.csv"
    with open(f"categories/{csv_filename}", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Créer un slug pour chaque catégorie
        slug = category.lower().replace(" ", "-")

        # URL de chaque catégorie
        page_url = f"http://books.toscrape.com/catalogue/category/books/{slug}_{category_id}/index.html"
        product_page_urls = []

        # Gérer la pagination
        while True:
            response = requests.get(page_url)
            if response.status_code != 200:
                print(f"Erreur : catégorie '{category}' introuvable.") 
                # Ne pas créer de fichier CSV si la catégorie n'existe pas
                csvfile.close()
                os.remove(f"categories/{csv_filename}")
                break

            soup = BeautifulSoup(response.content, "html.parser")
            books_url = soup.find_all("h3")
            for url in books_url:
                product_page_urls.append(urljoin(page_url, url.a["href"]))
            
            # Vérifier s'il y a une page suivante
            next_page = soup.find("li", class_="next")
            if next_page:
                next_page_url = next_page.a["href"]
                page_url = urljoin(page_url, next_page_url)
            else:
                break

        # Extraire les informations des livres de chaque catégorie
        for url in product_page_urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            
            try:
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

                # Extraire l'image de chaque livre au format .jpg en nommant le fichier avec le titre du livre et sa catégorie dans le dossier "images"
                image_filename = f"images/{category}_{title}.jpg"
                image_data = requests.get(image_url).content
                with open(image_filename, "wb") as image_file:
                    image_file.write(image_data)
                    print(f"Image enregistrée : {image_filename}")


                # Écrire les données dans le fichier CSV
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
                    "image_url": image_url,
                    "image_path": f"../{image_filename}"
                })
                print(f"Livre extrait : {title}")

            except Exception as e:
                print(f"Erreur lors de l'extraction d'un livre : {e}")

print("Extraction terminée.")