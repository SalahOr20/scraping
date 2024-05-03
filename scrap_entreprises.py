import json
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

url = 'https://annuaire-entreprises.data.gouv.fr/rechercher?terme=&cp_dep_label=Toulouse+%2831000%29&cp_dep_type=cp&cp_dep=31000&fn=&n=&dmin=&dmax=&type=&label=&etat=A&sap=D&sap=G&sap=J&sap=K&sap=O&naf=&nature_juridique=&tranche_effectif_salarie=&categorie_entreprise=GE&categorie_entreprise=ETI'

browser = webdriver.Firefox()

browser.get(url)
def get_infos_entreprise(links):
    infos_entreprises = []
    for link in links:

        browser.get(link)
        time.sleep(1)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            nom_entreprise = browser.find_element(by=By.XPATH,
                                                      value='//*[@id="entreprise"]/div[1]/div[1]/table/tbody/tr[1]/td[2]/button/span').text
        except Exception as e:
            print(f"Erreur lors de l'extraction du nom de l'entreprise : {e}")
            nom_entreprise = ""

        try:
            siren = browser.find_element(by=By.XPATH,
                                             value='//*[@id="entreprise"]/div[1]/div[1]/table/tbody/tr[2]/td[2]/button/span').text
        except Exception as e:
            print(f"Erreur lors de l'extraction du SIREN : {e}")
            siren = ""

        try:
            siret = browser.find_element(by=By.XPATH,
                                             value='//*[@id="entreprise"]/div[1]/div[1]/table/tbody/tr[3]/td[2]/button/span[1]').text
        except Exception as e:
            print(f"Erreur lors de l'extraction du SIRET : {e}")
            siret = ""

        try:
            tva = browser.find_element(by=By.XPATH, value='//*[@id="tva-cell-result"]').text
        except Exception as e:
            print(f"Erreur lors de l'extraction du numéro TVA : {e}")
            tva = ""

        try:
            activite = browser.find_element(by=By.XPATH,
                                                value='//*[@id="entreprise"]/div[1]/div[1]/table/tbody/tr[5]/td[2]/button/span').text
        except Exception as e:
            print(f"Erreur lors de l'extraction de l'activité : {e}")
            activite = ""

        try:
                adresse = browser.find_element(by=By.XPATH,
                                               value='//*[@id="entreprise"]/div[1]/div[1]/table/tbody/tr[7]/td[2]/button/span').text
        except Exception as e:
            print(f"Erreur lors de l'extraction de l'adresse : {e}")
            adresse = ""

        try:
            nature_juridique = browser.find_element(by=By.XPATH,
                                                         value='//*[@id="entreprise"]/div[1]/div[1]/table/tbody/tr[8]/td[2]/button/span').text
        except Exception as e:
            print(f"Erreur lors de l'extraction de la nature juridique : {e}")
            nature_juridique = ""

        try:
            effectifs = browser.find_element(by=By.XPATH,
                                                 value='//*[@id="entreprise"]/div[1]/div[1]/table/tbody/tr[9]/td[2]/button/span').text
        except Exception as e:
            print(f"Erreur lors de l'extraction des effectifs : {e}")
            effectifs = ""

        try:
            taille_entreprise = browser.find_element(by=By.XPATH,
                                                          value='//*[@id="entreprise"]/div[1]/div[1]/table/tbody/tr[10]/td[2]/button/span').text
        except Exception as e:
            print(f"Erreur lors de l'extraction de la taille de l'entreprise : {e}")
            taille_entreprise = ""

        try:
            date_creation = browser.find_element(by=By.XPATH,
                                                     value='//*[@id="entreprise"]/div[1]/div[1]/table/tbody/tr[11]/td[2]/button/span').text
        except Exception as e:
            print(f"Erreur lors de l'extraction de la date de création : {e}")
            date_creation = ""

        try:
            donnee_financiere = browser.find_element(by=By.XPATH,
                                                          value='/html/body/div[4]/main/div/div[1]/div[3]/div/a[5]')
            donnee_financiere.click()
            time.sleep(1)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            chiffre_affaire_text = browser.find_element(by=By.XPATH,
                                                       value='/html/body/div[4]/main/div/div[2]/div[1]/table/tbody/tr[3]/td[7]').text
            chiffre_affaire = chiffre_affaire_text.replace('€', '').strip()
        except Exception as e:
            print(f"Erreur lors de l'extraction du chiffre d'affaires : {e}")
            chiffre_affaire = ""

        infos_entreprise = {
                "Nom de la structure": nom_entreprise,
                'SIREN': siren,
                'SIRET du siège social': siret,
                'N° TVA Intracommunautaire': tva,
                'Activité principale (NAF/APE)': activite,
                'Adresse postale': adresse,
                'Nature juridique': nature_juridique,
                'Tranche effectif salarié de la structure': effectifs,
                'Taille de la structure': taille_entreprise,
                'Date de création': date_creation,
                'Chiffre d\'affaire': chiffre_affaire
            }

        for j in range(2):
            browser.back()
        print(infos_entreprise)
        infos_entreprises.append(infos_entreprise)


    with open('infos_entreprises.json', 'w') as f:
        json.dump(infos_entreprises, f, indent=4)

    return infos_entreprises
def pagination():

    links = []
    i = 0
    j=0
    while i < 11:
        i += 1

        try:
            link = browser.find_element(By.XPATH, f'/html/body/div[4]/main/div/div[2]/div[1]/div[{i}]/a')
            links.append(link.get_attribute('href'))
            print(link.get_attribute('href'))
        except NoSuchElementException:
            pass
        if i == 10:
            j+=1
            i = 0
            try:
                next_button = browser.find_element(By.XPATH, '/html/body/div[4]/main/div/div[2]/div[2]/nav/ul/li[9]/a')
                next_button.click()
            except NoSuchElementException:
                break
        if j==68:
            break

    print(links)
    return links




links=pagination()
get_infos_entreprise(links)
