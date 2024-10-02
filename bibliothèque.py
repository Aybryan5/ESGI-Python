import sqlite3

# Connexion à la base de données SQLite (ou création si elle n'existe pas)
conn = sqlite3.connect('bibliotheque.db')
cursor = conn.cursor()

# Créer la table des livres avec une colonne 'disponible'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS livres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL,
        disponible INTEGER DEFAULT 1 -- 1 = Disponible, 0 = Emprunté
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS emprunts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        livre_id INTEGER,
        FOREIGN KEY (livre_id) REFERENCES livres(id)
    )
''')

conn.commit()

class Bibliothèque:


    def addbook():
        book = input("Entrez le nom du livre à ajouter : ")
        cursor.execute("INSERT INTO livres (titre) VALUES (?)", (book,))
        conn.commit()
        print(f"Le livre '{book}' a été ajouté à la bibliothèque.")
        Bibliothèque.listbook()


    def listbook():
        cursor.execute("SELECT * FROM livres WHERE disponible = 1")
        books = cursor.fetchall()
        if books:
            print("\nListe des livres disponibles :")
            for i, livre in enumerate(books, 1):
                print(f"{i}. {livre[1]}")  # livre[1] est le titre
        else:
            print("Aucun livre disponible dans la bibliothèque.")
    

    def booktaken():
        Bibliothèque.listbook()
        
        # Récupération de tous les livres disponibles
        cursor.execute("SELECT * FROM livres WHERE disponible = 1")
        books = cursor.fetchall()

        if not books:
            print("Aucun livre disponible à l'emprunt.")
            return

        name = input("Entrez votre nom pour emprunter un livre : ")

        # Vérifier si la personne a déjà un emprunt en cours
        cursor.execute("SELECT * FROM emprunts WHERE nom = ?", (name,))
        emprunt_en_cours = cursor.fetchone()
        if emprunt_en_cours:
            print(f"{name}, vous avez déjà emprunté un livre et devez le rendre avant d'en emprunter un autre.")
            return

        try:
            index = int(input("Entrez le numéro du livre que vous souhaitez emprunter : ")) - 1
            if 0 <= index < len(books):
                book_id = books[index][0]  # Récupérer l'ID du livre
                cursor.execute("INSERT INTO emprunts (nom, livre_id) VALUES (?, ?)", (name, book_id))
                cursor.execute("UPDATE livres SET disponible = 0 WHERE id = ?", (book_id,))
                conn.commit()
                
                print(f"{name} a emprunté le livre '{books[index][1]}'.")
                Bibliothèque.list_emprunts()
            else:
                print("Numéro de livre invalide.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")



    def return_book():
        name = input("Entrez votre nom pour rendre un livre : ")

    # Vérifier si la personne a un emprunt en cours
        cursor.execute('''
            SELECT emprunts.id, livres.titre, livres.id FROM emprunts
            JOIN livres ON emprunts.livre_id = livres.id
            WHERE emprunts.nom = ?
        ''', (name,))
        emprunt = cursor.fetchone()

        if emprunt:
            print(f"{name} a rendu le livre '{emprunt[1]}'.")
            # Marquer le livre comme disponible
            cursor.execute("UPDATE livres SET disponible = 1 WHERE id = ?", (emprunt[2],))
            # Supprimer l'emprunt
            cursor.execute("DELETE FROM emprunts WHERE id = ?", (emprunt[0],))
            conn.commit()
        else:
            print(f"{name}, vous n'avez emprunté aucun livre.")


    def list_emprunts():
        cursor.execute('''
        SELECT emprunts.nom, livres.titre FROM emprunts
        JOIN livres ON emprunts.livre_id = livres.id
        ''')
        emprunts = cursor.fetchall()
        if emprunts:
            print("\nHistorique des emprunts :")
            for emprunt in emprunts:
                print(f"{emprunt[0]} a emprunté le livre '{emprunt[1]}'")
        else:
            print("Aucun emprunt en cours.")

def menu():
    while True:
        print("\nOptions :")
        print("1. Ajouter un livre")
        print("2. Lister les livres")
        print("3. Emprunter un livre")
        print("4. Rendre un livre")
        print("5. Voir l'historique des emprunts")
        print("6. Quitter")
        
        choix = input("Entrez le numéro de l'option choisie : ")
        
        if choix == '1':
            Bibliothèque.addbook()
        elif choix == '2':
            Bibliothèque.listbook()
        elif choix == '3':
            Bibliothèque.booktaken()
        elif choix == '4':
            Bibliothèque.return_book()
        elif choix == '5':
            Bibliothèque.list_emprunts()
        elif choix == '6':
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")


menu()


conn.close()
