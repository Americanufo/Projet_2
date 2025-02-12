# Projet Programme d'extraction des prix

## Prérequis 
Assurez-vous d'avoir installé Python 3.x et Pip.
Si ce n'est pas le cas vous pouvez installer Python ici : https://www.python.org

Vérifier si pip est installé via votre terminal en tapant la ligne de commande ci-dessous :
python3 -m pip --version
Si ce n'est pas le cas taper la ligne de commande :
curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
Puis exécuter le script Python :
python3 get-pip.py

## Installation de l'environnement virtuel

1. **Créer l'environnement virtuel**

Ouvrez votre terminal sur le dossier du projet puis exécuter la commande suivante pour créer l'environnement :
python3 -m venv env

2. **Activer l'environnement virtuel**

Exécuter la commande suivante :
source env/bin/activate

3. **Installer les bibliothèques nécessaires avec requirements.txt**

Exécuter la commande suivante :
pip install -r requirements.txt

4. **Pour sortir de l'environnement virtuel**

Exécuter la commande suivante:
deactivate

## Lancer le code 

1. **Exécuter le fichier main.py**

Exécuter la commande suivante :
python3 main.py

## Explication des autres scripts Python
Les scripts Python suivants m'ont été utiles pour développer mon code par étape tel que défini dans les étapes du projet :
- analyse_page_livre.py
- analyse_category_mystery.py 
