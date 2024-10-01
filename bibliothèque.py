import json
import os


SHELVES_FILE = './shelves.json'
EMPRUNTS_FILE = './emprunts.json'


def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []


def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


Shelves = load_data(SHELVES_FILE)
Emprunts = load_data(EMPRUNTS_FILE)

class Bibliothèque:

    
    def addbook():
        book = input("Entrez le nom du livre à ajouter : ")
        Shelves.append(book)
        save_data(SHELVES_FILE, Shelves)  
        print(f"Le livre '{book}' a été ajouté aux étagères.")
        Bibliothèque.listbook()

    
    def listbook():
        if Shelves:
            print("\nListe des livres disponibles :")
            for i, livre in enumerate(Shelves, 1):
                print(f"{i}. {livre}")
        else:
            print("Aucun livre disponible sur les étagères.")
    
    
    def booktaken():
        Bibliothèque.listbook()
        if not Shelves:
            return
        
        name = input("Entrez votre nom pour emprunter un livre : ")

        for emprunt in Emprunts:
            if emprunt['nom'] == name:
                print(f"{name}, vous avez déjà emprunté le livre '{emprunt['livre']}' et devez le rendre avant d'en prendre un autre.")
                return

        try:
            index = int(input("Entrez le numéro du livre que vous souhaitez emprunter : ")) - 1
            if 0 <= index < len(Shelves):
                emprunt = {
                    'nom': name,
                    'livre': Shelves[index]
                }
                Emprunts.append(emprunt)
                save_data(EMPRUNTS_FILE, Emprunts)  
                
                print(f"{name} a emprunté le livre '{Shelves[index]}'.")
                Shelves.pop(index)  
                save_data(SHELVES_FILE, Shelves)  

                Bibliothèque.list_emprunts()  
            else:
                print("Numéro de livre invalide.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")
    
    def returnbook():
        name = input("Entrez votre nom pour rendre un livre : ")

        
        for emprunt in Emprunts:
            if emprunt['nom'] == name:
                print(f"{name} a rendu le livre '{emprunt['livre']}'.")
                Shelves.append(emprunt['livre'])  
                Emprunts.remove(emprunt)  
                save_data(SHELVES_FILE, Shelves) 
                save_data(EMPRUNTS_FILE, Emprunts)  
                return

        print(f"{name}, vous n'avez emprunté aucun livre.")
    
    def list_emprunts():
        if Emprunts:
            print("\nHistorique des emprunts :")
            for emprunt in Emprunts:
                print(f"{emprunt['nom']} a emprunté le livre '{emprunt['livre']}'")
        else:
            print("Aucun emprunt en cours.")


def menu():
    while True:
        print("\nOptions :")
        print("1. Ajouter un livre")
        print("2. Lister les livres")
        print("3. Emprunter un livre")
        print("4. Voir l'historique des emprunts")
        print("5. Rendre un livre")
        print("6. Quitter")
        
        choix = input("Entrez le numéro de l'option choisie : ")
        
        if choix == '1':
            Bibliothèque.addbook()
        elif choix == '2':
            Bibliothèque.listbook()
        elif choix == '3':
            Bibliothèque.booktaken()
        elif choix == '4':
            Bibliothèque.list_emprunts()
        elif choix == '5':
            Bibliothèque.returnbook()
        elif choix == '6':
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")


menu()
