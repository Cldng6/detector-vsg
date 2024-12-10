## Créer un nouvel environnement virtuel

    python3 -m venv tester
    
## Activer l'environnement virtuel
    source tester/bin/activate  

## Installer des packages dans l'environnement virtuel
    pip install opencv-python
    pip install mysql-connector-python
    pip3 install dlib

## executer le script dans l'environnement virtuel
    python visage-detector.py

## Vérifier que l'environnement virtuel fonctionne
    pip list

## Désactiver l'environnement virtuel lorsque vous avez terminé
    deactivate

## Supprimer l'environnement virtuel
    rm -rf nom_de_votre_environnement


# Creation de database
    assure vous que database est deja installer...

    mysql -u root -p
        """
            CREATE DATABASE tester_db;

            USE tester_db;

            CREATE TABLE faces (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                face_encoding BLOB NOT NULL
            );
        """


En dev....................................................
