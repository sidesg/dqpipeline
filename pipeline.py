#TODO: Add logging, more flexible fields for resource update

from ckanapi import RemoteCKAN
import yaml
import lib as lb
from lib import CKANResource

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
            resource = CKANResource(lb.get_resource(ress_id, conn))
            resource.update_file("data/" + path, conn)


if __name__ == "__main__":
    main()
    