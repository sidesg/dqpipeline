from ckanapi import RemoteCKAN
import json
import os

def get_package(id, connexion: RemoteCKAN) -> dict:
    package = connexion.call_action("package_show", {"id": id})
    
    return package

def get_resource(id, connexion: RemoteCKAN) -> dict:
    resource = connexion.call_action("resource_show", {"id": id})
    
    return resource

class CKANGeneral():
    def __init__(self, data: dict = dict()) -> None:
        self.data: dict = data
        self.id = self.data.get("id", None)
    
    def __repr__(self) -> str:
        return json.dumps(self.data, indent=4, ensure_ascii=False)
    
    def write_json(self, path: str) -> None:
        with open(path, "w", encoding="utf8") as f:
            f.write(self.__repr__())
    
class CKANPackage(CKANGeneral):
    def update_title(self, title: str, conn: RemoteCKAN):
        conn.call_action(
            "package_patch",
            {
                "id": self.id,
                "title": title
            }
        )

    def new_resource(self, path: str, conn: RemoteCKAN):
        conn.call_action("resource_create",
            {
                "package_id": self.id,
                "name": "Ressource test",
                "url": "test",
                "description": "test",
                "taille_entier": 1,
                "resource_type": "donnees",
                "relidi_condon_valinc": "oui",
                "format": "JSON"
                },
            files={"upload": open(path, "rb")}
        )

class CKANResource(CKANGeneral):
    def update_file(self, path: str, conn: RemoteCKAN):
        file_size = int(round(os.stat(path).st_size / (1024 * 1024), 0))
        
        conn.call_action(
            "resource_patch",
            {
                "id": self.id,
                "taille_entier": file_size
            },
            files={"upload": open(path, "rb")}
        )
        