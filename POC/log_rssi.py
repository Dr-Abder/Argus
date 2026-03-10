import subprocess # pour lancer les commandes windows
import time # gestion du temps
import csv # écriture fichier Excel/CSC
from datetime import datetime # heure exacte

def capture_wifi_data():

    """
    Cette fonction récupère les informations de l'interface Wi-Fi sous Windows.

    1) Commande exécutée par Python dans le terminal Windows :

        commande = ["netsh", "wlan", "show", "interfaces"]

       Cette commande affiche les informations du Wi-Fi dont nous avons besoin
       (SSID, signal, canal, etc.).

    2) Exécution de la commande système avec subprocess.run() :

        resultat = subprocess.run(
            commande,            # commande à exécuter
            capture_output=True, # stocke la sortie de la commande
            text=True,           # retourne le résultat sous forme de texte
            encoding="utf-8",    # force l'encodage UTF-8
            errors="ignore"      # ignore les erreurs d'encodage éventuelles
        )

    3) Création d'un dictionnaire vide pour stocker les informations :

        info_brutes = {}

    4) Parcours du texte ligne par ligne :

        for ligne in resultat.stdout.splitlines():

       - resultat.stdout contient tout le texte retourné par la commande.
       - splitlines() découpe ce texte ligne par ligne.

    5) Vérification que la ligne contient une clé :

        if ":" in ligne

       Les informations sont au format : clé : valeur.

    6) Séparation de la clé et de la valeur :

        cle, valeur = ligne.split(":", 1)

       Le "1" signifie que la séparation se fait uniquement au premier ":".

    7) Nettoyage et stockage dans le dictionnaire :

        info_brutes[cle.strip()] = valeur.strip()

       strip() permet de supprimer les espaces inutiles avant et après le texte.

    8) La fonction retourne finalement le dictionnaire contenant toutes les
       informations Wi-Fi récupérées.
    """

    commande = ["netsh.exe", "wlan", "show", "interfaces"]
    resultat = subprocess.run(commande, capture_output=True, text=True,
                              encoding="utf-8", errors="ignore")

    # dictionnaire vide pour ranger les infos
    info_brutes = {}

    # découpe le texte ligne par ligne
    for ligne in resultat.stdout.splitlines():
        if ":" in ligne:
            # sépare la ligne en deux
            cle, valeur = ligne.split(":", 1)
            # nettoyage des espaces et rangement dans le ditionnaire
            info_brutes[cle.strip()] = valeur.strip()

    return info_brutes


def extraire_mesure(data_dict):

    """
    Cette fonction extrait les informations utiles du dictionnaire contenant
    les données Wi-Fi brutes récupérées par la commande système.

    1) Recherche intelligente du BSSID :

        bssid_trouve = "N/A"

       Le BSSID peut apparaître sous différents noms selon la langue du système
       ou la configuration (par exemple "Point d'accès" ou "BSSID").

       On parcourt donc toutes les clés du dictionnaire :

        for cle in data_dict.keys():

       Si l'une des clés contient "Point d'accès" ou "BSSID", on considère
       que c'est l'information recherchée.

        if "Point d'accès" in cle or "BSSID" in cle:

       La valeur correspondante est alors récupérée :

        bssid_trouve = data_dict[cle]

       Puis on arrête immédiatement la boucle avec :

        break

       Cela évite de continuer à parcourir inutilement les autres clés.

    2) Extraction des informations principales :

       On construit un nouveau dictionnaire contenant uniquement les mesures
       utiles pour le programme.

       La méthode .get(cle, valeur_par_defaut) est utilisée afin d'éviter
       que le programme plante si une information est absente.

       Exemple :

        data_dict.get("SSID", "N/A")

       Si la clé "SSID" existe, sa valeur est retournée.
       Sinon, la valeur par défaut "N/A" est utilisée.

    3) Dictionnaire final des mesures :

        mesures = {
            "ssid": data_dict.get("SSID", "N/A"),
            "etat": data_dict.get("État", "Déconnecté"),
            "signal": data_dict.get("Signal", "0%"),
            "bssid": bssid_trouve,
            "rssi": data_dict.get("Rssi", "0")
        }

       Ce dictionnaire contient les informations principales du réseau Wi-Fi.

    4) La fonction retourne finalement ce dictionnaire de mesures.
    """

    # cherche le BSSID intelligemment
    bssid_trouve = "N/A"
    for cle in data_dict.keys():
        # Si le mot "Point d'accès" ou "BSSID" est dans la clé
        if "Point d'accès" in cle or "BSSID" in cle:
            bssid_trouve = data_dict[cle]
            break # s'arrête dès qu'on a trouvé
    
    # .get(cle, defaut) permet de ne pas planter si l'info manque
    mesures = {
        "ssid": data_dict.get("SSID", "N/A"),
        "etat": data_dict.get("État", "Déconnecté"),
        "signal": data_dict.get("Signal", "0%"),
        "bssid": bssid_trouve,
        "rssi": data_dict.get("Rssi", "0")
    }

    return mesures

def main():

    """
    Fonction principale du script. Elle permet d'enregistrer des mesures Wi-Fi
    dans un fichier CSV pendant une durée déterminée.

    1) Configuration de la session :

        label = input("Nom de la session (ex: couloir_calme)")
        durée = int(input("Combien de secondes"))

       L'utilisateur choisit un nom de session et une durée d'enregistrement.
       Le nom sera utilisé pour générer le fichier de données.

       Exemple :
           data_couloir_calme.csv

       On enregistre également l'heure de début :

           temps_debut = time.time()

       Cela permettra de mesurer le temps écoulé.

    2) Ouverture du fichier CSV :

        with open(nom_fichier, "w", newline="", encoding="utf-8-sig") as f:

       Le fichier est ouvert en mode écriture ("w").
       L'encodage UTF-8 permet d'éviter les problèmes de caractères.

       On crée ensuite un objet writer pour écrire dans le fichier :

           writer = csv.writer(f, delimiter=';')

       Le séparateur utilisé est ";" afin d'être compatible avec Excel.

       On écrit ensuite les titres des colonnes :

           writer.writerow([
               "Horodatage",
               "Seconde",
               "SSID",
               "Etat",
               "Signal",
               "BSSID",
               "RSSI"
           ])

    3) Boucle de collecte des données :

        while (time.time() - temps_debut) < durée:

       La boucle s'exécute tant que la durée définie n'est pas dépassée.

       À chaque itération :

       - On récupère les informations Wi-Fi brutes :

            infos = capture_wifi_data()

       - On extrait les mesures utiles :

            m = extraire_mesure(infos)

       - On génère un horodatage précis :

            horodatage = datetime.now().strftime("%H:%M:%S.%f")[:-3]

         Cela donne une précision à la milliseconde.

       - On calcule le temps écoulé depuis le début :

            secondes_ecoulees = round(time.time() - temps_debut, 2)

    4) Création de la ligne de données :

        ligne = [
            horodatage,
            secondes_ecoulees,
            m['ssid'],
            m['etat'],
            m['signal'],
            m['bssid'],
            m['rssi']
        ]

       Cette ligne contient toutes les mesures collectées.

    5) Écriture et affichage :

       La ligne est :

       - enregistrée dans le fichier CSV :

            writer.writerow(ligne)

       - affichée dans le terminal pour suivre les mesures en temps réel :

            print(f"[{secondes_ecoulees}s] SSID: {m['ssid']} | Signal: {m['signal']}% | RSSI: {m['rssi']}")

    6) Pause entre deux mesures :

        time.sleep(0.1)

       Une pause de 0,1 seconde est ajoutée afin d'éviter de surcharger
       le processeur et de limiter la fréquence des mesures.

    7) Fin de l'enregistrement :

       Une fois la durée atteinte, la boucle s'arrête et le fichier est fermé.

       Un message confirme la fin de la session :

           "Terminé ! Fichier enregistré : nom_fichier"
    """

    # 1. Configuration
    label = input("Nom de la session (ex: couloir_calme) : ")
    durée =int(input("Combien de secondes : "))
    
    nom_fichier = f"data_test_{label}.csv"
    temps_debut = time.time()

    # 2. Ouverture du fichier
    with open(nom_fichier, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=';')
        # les titres des colonnes
        writer.writerow(["Horodatage", "Seconde", "SSID", "Etat", "Signal", "BSSID", "RSSI"])
    
        # 3. boucle de travail
        while (time.time() - temps_debut) < durée:
            infos = capture_wifi_data()
            m = extraire_mesure(infos) # On l'appelle 'm' pour que tes lignes suivantes marchent

            horodatage = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            secondes_ecoulees = round(time.time() - temps_debut, 2)

            # On prépare la ligne
            ligne = [horodatage, secondes_ecoulees, m['ssid'], m['etat'], m['signal'], m['bssid'], m['rssi']]
            
            # On écrit dans le fichier et on affiche sur l'écran
            writer.writerow(ligne)
            print(f"[{secondes_ecoulees}s] SSID: {m['ssid']} | Signal: {m['signal']}% | RSSI: {m['rssi']}")
            
            # Petite pause pour ne pas surcharger le processeur
            time.sleep(0.1)

    print(f"Terminé ! Fichier enregistré : {nom_fichier}")

# Pour lancer le script
if __name__ == "__main__":
    main()