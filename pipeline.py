import yaml
import logging
import shutil

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
    logging.basicConfig(filename=(logfolder / f'pipeline-{timestamp}.log'), encoding='utf-8', level=logging.DEBUG)

    #Load dict of resource-file key-value pairs
    with open('updates.yml', 'r') as file:
        updates: dict = yaml.safe_load(file)

    #Load API key
    keypath = ".creds/apikey.txt"
    if not Path(keypath).exists():
        createkey()
    ua = 'cmtq/1.0 (+https://www.cinematheque.qc.ca/)'

    with open(keypath, "r") as infile:
        apikey: str = infile.read()

    #Upload files
    with RemoteCKAN('https://www.donneesquebec.ca', 
                    user_agent=ua, apikey=apikey) as conn:
        for ress_id, path in updates.items():
            fullpath: str = "data/" + path
            try:
                resource = CKANResource.from_id(ress_id, conn)
            except Exception:
                logging.error(f"\"{ress_id}\". Identifiant de ressource introuvable sur Données Québec")
                continue

            if not Path(fullpath).exists():
                logging.error(f"\"{ress_id}\" : \"{path}\" chemin de fichier invalide")
                continue

            try:
                resource.update_file(fullpath, conn)
            except Exception:
                logging.error(f"\"{ress_id}\" : \"{path}\" échec de la mise à jour")
                continue

            shutil.move(fullpath, "uploaded")
            logging.info(f"{path} déplacé au dossier 'uploaded'")

def createkey() -> None:
    keyfolder = Path(".creds")
    keyfolder.mkdir()
    apikey = input("Saisir votre cle API : ").strip()

    with open(keyfolder / "apikey.txt", "w") as f:
        f.write(apikey)


if __name__ == "__main__":
    main()
    