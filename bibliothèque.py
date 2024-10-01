Shelves = ['Livre1', 'Livre2', 'Livre3', 'Livre4', 'Livre5']
Emprunts = []

class Bibliothèque:
    def addbook():
        book = input("Entrez votre livre")
        Shelves.append(book)
        print(Shelves)

    
    def listbook():
        if Shelves : 
            for i in range(len(Shelves)):
                print(f"{i+1}. {Shelves[i]}")
        else:
            print("Aucun livre disponible sur les étagères.")

    def booktaken():
        Bibliothèque.listbook()
        if not Shelves:
            return  
        index = int(input("Entrez le numéro du livre que vous souhaitez emprunter : ")) - 1
        if 0 <= index < len(Shelves):  
            name = input("Entrez votre nom pour emprunter le livre : ")
            
            emprunt = {
                'nom': name,
                'livre': Shelves[index]
            }
            Emprunts.append(emprunt)
    
            print(f"{name} a emprunté le livre '{Shelves[index]}'.")
            Shelves.pop(index)  

            print("\nHistorique des emprunts :")
            for emprunt in Emprunts:
                print(f"{emprunt['nom']} a emprunté le livre '{emprunt['livre']}'")
        else:
            print("Numéro de livre invalide.")



Bibliothèque.addbook()
Bibliothèque.booktaken()
Bibliothèque.listbook()