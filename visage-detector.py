import cv2
import numpy as np
import dlib
import mysql.connector
from mysql.connector import Error

# Fonction pour se connecter à la base de données MySQL
def connect_to_db():
    try:
        # Remplacez les informations suivantes par vos propres informations de connexion
        connection = mysql.connector.connect(
            host='localhost',  # Nom du serveur MySQL
            database='tester_db',  # Nom de la base de données MySQL
            user='root',  # Nom d'utilisateur MySQL
            password='mot de passe'  # Votre mot de passe MySQL
        )
        if connection.is_connected():
            print("Connexion réussie à la base de données")
        return connection
    except Error as e:
        print("Erreur lors de la connexion à la base de données", e)
        return None

# Fonction pour charger les visages et noms de la base de données
def load_known_faces_from_db(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name, face_encoding FROM faces")
    rows = cursor.fetchall()

    known_face_encodings = []
    known_face_names = []

    for row in rows:
        name = row[0]
        face_encoding = np.frombuffer(row[1], dtype=np.float64)
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)

    return known_face_encodings, known_face_names

# Fonction pour enregistrer un nouveau visage dans la base de données
def save_face_to_db(connection, name, face_encoding):
    cursor = connection.cursor()
    face_encoding_blob = face_encoding.tobytes()  # Convertir l'encodage en BLOB pour MySQL
    cursor.execute("INSERT INTO faces (name, face_encoding) VALUES (%s, %s)", (name, face_encoding_blob))
    connection.commit()

# Initialisation de la webcam
cap = cv2.VideoCapture(0)

# Chargement du détecteur de visages dlib
detector = dlib.get_frontal_face_detector()

# Connexion à la base de données
connection = connect_to_db()

# Charger les visages connus depuis la base de données
known_face_encodings, known_face_names = load_known_faces_from_db(connection)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir l'image en niveaux de gris pour la détection des visages
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détection des visages dans l'image
    faces = detector(gray)

    # Pour chaque visage détecté, ajouter un rectangle et essayer de l'identifier
    for face in faces:
        # Extraire les coordonnées du rectangle de chaque visage détecté
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())
        
        # Découper l'image du visage détecté
        face_encoding = frame[y:y+h, x:x+w]
        face_encoding = cv2.cvtColor(face_encoding, cv2.COLOR_BGR2RGB)
        
        # Comparer le visage avec les visages connus dans la base de données
        name = "Inconnu"
        for known_face_encoding, known_name in zip(known_face_encodings, known_face_names):
            # Comparer l'encodage du visage détecté avec les encodages connus
            if np.allclose(face_encoding.flatten(), known_face_encoding):
                name = known_name
                break

        # Dessiner un rectangle autour du visage et afficher le nom
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, name, (x + 6, y + h - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Afficher l'image avec les visages détectés
    cv2.imshow("Face Detection", frame)

    # Quitter en appuyant sur 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la caméra et fermer la fenêtre
cap.release()
cv2.destroyAllWindows()

# Fermer la connexion à la base de données
if connection.is_connected():
    connection.close()
    print("Connexion à la base de données fermée")
