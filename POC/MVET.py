import pandas as pd  # Import pandas pour manipuler les données tabulaires (CSV)

def analyse_rssi(fichier):
    """
    Analyse statistique simple d'un fichier contenant des mesures RSSI.

    Paramètre :
        fichier (str) : chemin vers le fichier CSV contenant les données RSSI.

    Le script calcule :
        - la moyenne du RSSI
        - la variance du signal
        - l'écart-type

    Ces indicateurs permettent d'observer la stabilité ou l'instabilité du signal
    Wi-Fi et donc d'inférer la présence éventuelle d'un mouvement dans la zone.
    """

    # Lecture du fichier CSV avec pandas
    # Le séparateur utilisé dans les fichiers est ";"
    df = pd.read_csv(fichier, delimiter=";")

    # Extraction de la colonne RSSI et conversion en entier
    # (certaines lectures CSV peuvent importer les valeurs comme texte)
    if "RSSI_dBM" in df.columns:
        rssi = df["RSSI_dBm"].astype(int)
    else:
        rssi = df["RSSI"].astype(int)

    # Calcul de la moyenne du RSSI
    # Permet d'observer une éventuelle atténuation du signal
    moyenne = rssi.mean()

    # Calcul de la variance
    # Indicateur clé : une variance élevée signifie un signal instable
    # (souvent causé par un mouvement dans la zone de propagation)
    variance = rssi.var()

    # Calcul de l'écart-type (racine carrée de la variance)
    # Mesure la dispersion du signal autour de la moyenne
    ecart_type = rssi.std()

    # Affichage des résultats
    print("Analyse du fichier :", fichier)
    print("Nombre de mesures :", len(rssi))
    print("Moyenne RSSI :", round(moyenne, 2), "dBm")
    print("Variance :", round(variance, 2))
    print("Écart-type :", round(ecart_type, 2))
    print("-" * 40)


# Analyse des deux conditions expérimentales :

# 1. Pièce calme (référence / silence environnemental)
print("Analyse sans sujet")
analyse_rssi(input("Emplacement du fichier (ex: data_test/couloir) : "))

print("Analyse avec sujet")
# 2. Passage d'une personne dans la ligne de visée
analyse_rssi(input("Emplacement du fichier (ex: data_test/couloir) : "))