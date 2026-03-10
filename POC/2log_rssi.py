import subprocess
import time
import csv
from datetime import datetime


INTERFACE = "wlan0"  # ⚠️ adapte si nécessaire


def capture_wifi_data():
    """
    Récupère les informations Wi-Fi sous Kali Linux
    en utilisant la commande : iw dev wlan0 link
    """

    commande = ["iw", "dev", INTERFACE, "link"]

    resultat = subprocess.run(
        commande,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    info = {
        "ssid": "N/A",
        "signal": "0",
        "bssid": "N/A",
        "rssi": "0",
        "etat": "Déconnecté"
    }

    sortie = resultat.stdout

    if "Connected to" in sortie:
        info["etat"] = "Connecté"

        for ligne in sortie.splitlines():

            if "Connected to" in ligne:
                # Exemple : Connected to 00:11:22:33:44:55 (on wlan0)
                info["bssid"] = ligne.split()[2]

            if "SSID:" in ligne:
                info["ssid"] = ligne.split("SSID:")[1].strip()

            if "signal:" in ligne:
                # Exemple : signal: -45 dBm
                signal_dbm = ligne.split("signal:")[1].strip().split()[0]
                info["rssi"] = signal_dbm
                info["signal"] = signal_dbm  # ici on garde dBm

    return info


def main():

    label = input("Nom de la session (ex: couloir_calme) : ")
    duree = int(input("Combien de secondes : "))

    nom_fichier = f"data_{label}.csv"
    temps_debut = time.time()

    with open(nom_fichier, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([
            "Horodatage",
            "Seconde",
            "SSID",
            "Etat",
            "Signal_dBm",
            "BSSID",
            "RSSI_dBm"
        ])

        while (time.time() - temps_debut) < duree:

            m = capture_wifi_data()

            horodatage = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            secondes_ecoulees = round(time.time() - temps_debut, 2)

            ligne = [
                horodatage,
                secondes_ecoulees,
                m['ssid'],
                m['etat'],
                m['signal'],
                m['bssid'],
                m['rssi']
            ]

            writer.writerow(ligne)

            print(
                f"[{secondes_ecoulees}s] "
                f"SSID: {m['ssid']} | "
                f"Signal: {m['signal']} dBm | "
                f"RSSI: {m['rssi']} dBm"
            )

            time.sleep(0.5)

    print(f"Terminé ! Fichier enregistré : {nom_fichier}")


if __name__ == "__main__":
    main()