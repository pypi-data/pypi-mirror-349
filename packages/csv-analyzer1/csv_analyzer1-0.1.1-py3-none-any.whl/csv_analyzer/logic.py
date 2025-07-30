import csv
from .models import Client
from typing import List

def analyser_csv(fichier: str) -> List[Client]:
    clients = []
    with open(fichier, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for ligne in reader:
            try:
                client = Client(
                    id=int(ligne['id']),
                    name=ligne['name'],
                    email=ligne['email'],
                    age=int(ligne['age']) if ligne['age'] else None
                )
                clients.append(client)
            except Exception as e:
                print(f"Erreur pour la ligne {ligne}: {e}")
    return clients
