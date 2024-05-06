import json

import pandas as pd
import requests
import time

def get_offres(domaine, region):
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    headers = {
        "Authorization": "Bearer FtM7onikDqyRObdadsvtlF-LBhg",
        "Accept": "application/json"
    }

    offres = []

    for nature_contrat in ["E1", "E2"]:
        querystring = {"domaine": domaine, "region": region, "natureContrat": nature_contrat}
        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            offres.extend(data['resultats'])
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête pour le domaine {domaine} et la nature du contrat {nature_contrat}: {e}")


        time.sleep(1)

    return offres


def convert_data_to_excel(data):
    if not data:
        print("Aucune donnée à exporter.")
        return

    df = pd.DataFrame(data)
    df_entreprises = df['entreprise'].apply(pd.Series)

    with pd.ExcelWriter('resultats_offres_emploi.xlsx') as writer:
        df.to_excel(writer, sheet_name='Offres d\'emploi', index=False)
        df_entreprises.to_excel(writer, sheet_name='Entreprises', index=False)

    print("Les données ont été exportées avec succès vers 'resultats_offres_emploi.xlsx'.")


domaines = {"M17": "Marketing", "M18": "Informatique", "G14": "Gestion et direction",
            "H12": "Conception, recherche, études et développement","C11":"Assurance","C12":"Banque","C13":"Finance","F11":"Conception et études","G13":"Conception, commercialisation et vente de produits touristiques","I16":"Véhicules, engins, aéronefs","K17":"Défense, sécurité publique et secours","M15":"Ressources humaines","M16":"Secrétariat et assistance","N21":"Personnel navigant du transport aérien","N31":"Personnel navigant du transport maritime et fluvial"}
region = "76"  # Région Occitanie

all_offres = []
for domaine, domaine_nom in domaines.items():
    print(f"Recherche des offres pour le domaine '{domaine_nom}'...")
    offres = get_offres(domaine, region)
    all_offres.extend(offres)





convert_data_to_excel(all_offres)

