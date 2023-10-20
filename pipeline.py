import yaml
import logging

from ckanapi import RemoteCKAN
from pathlib import Path
from datetime import datetime

from lib import CKANResource

def main():
    #Set up logging
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    logfolder = Path("logs")
    if not logfolder.exists():
        logfolder.mkdir()
    logging.basicConfig(filename=f'logs/pipeline-{timestamp}.log', encoding='utf-8', level=logging.DEBUG)

    keypath = ".creds/apikey.txt"
    if not Path(keypath).exists():
        createkey()
    ua = 'cmtq/1.0 (+https://www.cinematheque.qc.ca/)'

    with open('updates.yml', 'r') as file:
        updates: dict = yaml.safe_load(file)

    with open(keypath, "r") as infile:
        apikey = infile.read()

    with RemoteCKAN('https://www.donneesquebec.ca', 
                    user_agent=ua, apikey=apikey) as conn:
        for ress_id, path in updates.items():
            try:
                resource = CKANResource.from_id(ress_id, conn)
            except Exception:
                logging.error(f"\"{ress_id}\". identifiant de ressource introuvable")
                continue

            if not Path("data/" + path).exists():
                logging.error(f"\"{ress_id}\" : \"{path}\" chemin invalide")
                continue

            try:
                resource.update_file("data/" + path, conn)
            except Exception:
                logging.error(f"\"{ress_id}\" : \"{path}\" échec de la mise à jour")
                continue

def createkey():
    keyfolder = Path(".creds")
    keyfolder.mkdir()
    apikey = input("Saisir votre cle API : ").strip()

    with open(keyfolder / "apikey.txt", "w") as f:
        f.write(apikey)

if __name__ == "__main__":
    main()
    