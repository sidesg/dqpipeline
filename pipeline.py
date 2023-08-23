from ckanapi import RemoteCKAN
import yaml
import lib as lb
from lib import CKANPackage, CKANResource

def main():
    keypath = ".creds/apikey.txt"
    ua = 'cmtq/1.0 (+https://www.cinematheque.qc.ca/fr/)'

    with open('updates.yml', 'r') as file:
        updates = yaml.safe_load(file)

    with open(keypath, "r") as infile:
        apikey = infile.read()

    for ress_id, path in updates.items():
        with RemoteCKAN('https://www.donneesquebec.ca', 
                        user_agent=ua, apikey=apikey) as conn:
            test = CKANResource(lb.get_resource(ress_id, conn))
            test.update_file("data/" + path, conn)


if __name__ == "__main__":
    main()