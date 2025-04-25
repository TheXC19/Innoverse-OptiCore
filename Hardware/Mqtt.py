import threading
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time

# Configuration du broker HiveMQ Cloud
broker = "45d5baf312584b5eb0528a6426b0d145.s1.eu.hivemq.cloud"
port = 8883  # Port pour TLS/SSL
username = "essai"
password = "Mot_de_passe_2003"
topic = "nombre_passager"

# Fonction pour publier des messages en continu
def publier():
    while True:
        time.sleep(0.5)
        message = input("Entrez le message à envoyer : \n")
        publish.single(
            topic,
            payload=message,
            hostname=broker,
            port=port,
            auth={"username": username, "password": password},
            tls={"insecure": True}
        )

# Fonction de rappel appelée lorsqu'une connexion est établie
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        #print("Connecté avec succès au broker.")
        client.subscribe(topic)
        #print(f"Abonné au topic : {topic}")
    else:
        print(f"Échec de la connexion, code de retour : {rc}")

# Fonction de rappel appelée lorsqu'un message est reçu
def on_message(client, userdata, msg):
    print(f"Message reçu sur le topic '{msg.topic}': {msg.payload.decode()}")

# Création de l'instance du client MQTT
client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set()
client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message

# Lancement du thread de publication
thread1 = threading.Thread(target=publier)
thread1.daemon = True  # Permet d'arrêter le thread quand le programme principal se termine
thread1.start()

# Connexion au broker
#print("Tentative de connexion au broker...")
try:
    client.connect(broker, port)
except Exception as e:
    print(f"Erreur lors de la connexion : {e}")
    exit(1)

# Boucle infinie pour recevoir les messages
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Arrêt de l'abonnement.")
    client.disconnect()
