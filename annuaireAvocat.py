import re
import requests
from bs4 import BeautifulSoup

# je donne mon url :
# r = requests.get('https://www.barreaudenice.com/annuaire/avocats/?fwp_paged=1')

# verifie si ma requests est valide si status code = 200 :
# print(r.status_code)


# ================ function tourner pages =======================
def voirLesPages():
    # variable compteuse de pages :
    page_number = 1
    # creation d'une liste vide, je vais stocker tous mes urls dedans
    urls = []
    # boucle qui va changer l'url de la page :
    for i in range(163):
        # url avc f-strings on va changer uniquement la variable qui correspond au num de la page
        i = f"https://www.barreaudenice.com/annuaire/avocats/?fwp_paged={page_number}"
        # incrémentation de page_number
        page_number += 1
        # a chaque boucle je rajoute l'element i dans dans la liste grace a la method intégré append
        urls.append(i)

    return urls

# ====================================================================================

# appel function pour tester
# voirLesPages()


# ================ function qui va permettre extraction avocats ================
def extractionAvocats(url):
    # creation d'une variable qui envoi une request HTTP GET à l'url spécifié
    r = requests.get(url)

    # creation variable soup qui va recevoir le code html du site
    soup = BeautifulSoup(r.content, "html.parser")

    # variable qui va recuperer les infos de chaque div que je veux recup
    avocats = soup.find_all("div", class_="callout secondary annuaire-single")

    # boucle for qui va ns permettre de recup chaque balise interressante
    for avocat in avocats:
        # variable qui vont stocker les données des balise voulu
        nom = avocat.find("h3", class_='nom-prenom').text.strip()
        adresse = avocat.find("span", class_='adresse').text.strip()
        try:
            telephone = avocat.find("span", class_='telephone').text.strip()
        except AttributeError:
            telephone = ""
        try:
            email = avocat.find("span", class_='email').a.text.strip()
        except AttributeError:
            email = ""

        # nettoyage des variable avec regex pour nettoyage des espaces
        # Enlever les espaces supplémentaires & le T pour le telephone
        # try + except pour gerer cas ou vide
        try:
            nom_finale = re.sub(r"\s+", " ", nom).strip()
        except AttributeError as e :
            nom_finale = ""
        try:
            adress_finale = re.sub(r"\s+", " ", adresse).strip()
        except AttributeError as e:
            adress_finale = ""
        try:
            telephone_finale = re.sub(r"\s+|T", " ", telephone).strip()
        except AttributeError as e:
            telephone_finale = ""
        try:
            email_finale = re.sub(r"\s+", " ", email).strip()
        except AttributeError as e:
            email_finale = ""
        # creation d'une variable pour stocker le chemin
        # utilisation du row string => permet de negliger les slash dans mon chemin
        chemin = r"/Users/ismailbk/Desktop/ProjetScrapp-annuaireAvocat/fichier_scrapping.txt"

        # Ouvre et envoi les données scrappé dans le fichier chemin
        with open(chemin, "a") as f:
            f.write(f"\n{nom_finale}\n")
            f.write(f"{adress_finale}\n")
            f.write(f"{telephone_finale}\n")
            f.write(f"{email_finale}\n\n")


# ================================================================================
# appel function pour test
# extractionAvocats()

# ================================================================================

# ======= function qui va permettre extraction avocats de TOUTES LES PAGES ========

def parse_all_avocats():
    # creation variable pour recup le tableau avec tous les urls
    pages = voirLesPages()


    for page in pages:
        extractionAvocats(url=page)
        print (f"On scape {page}")


parse_all_avocats()