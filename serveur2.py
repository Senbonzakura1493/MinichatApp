# Définition d'un serveur réseau gérant un système de CHAT simplifié.
# Utilise les threads pour gérer les connexions clientes en parallèle.
 
HOST = 'localhost'
PORT = 4600
 
import socket, sys, threading


 
class ThreadClient(threading.Thread):
  '''dérivation d'un objet thread pour gérer la connexion avec un client'''
  def __init__(self, conn):
      threading.Thread.__init__(self)
      self.connexion = conn
      self.pseudo =""
 
  def run(self):
      # Dialogue avec le client :
      nom = self.getName()
      i=1
      while i==1: 
                  
        msgClient = self.connexion.recv(1024).decode("Utf8")
        
        pseudo = msgClient
        i+=1
          
      while i>1: 
                  
        msgClient = self.connexion.recv(1024).decode("Utf8")
        
          
        if not msgClient or msgClient.upper() =="FIN":
            break
        message = "%s> %s> %s" % (nom,pseudo, msgClient)
        print(message)
          # Faire suivre le message à tous les autres clients :
        for cle in conn_client:
            
          if cle != nom:
              # ne pas le renvoyer à l'émetteur
            conn_client[cle].send(message.encode("Utf8"))
            i+=1
        
 
        # Fermeture de la connexion :
      self.connexion.close()	  # couper la connexion côté serveur
      del conn_client[nom]	# supprimer son entrée dans le dictionnaire
      print("Client %s déconnecté." % nom)
	  
 

try:
  mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initialisation server
  mySocket.bind((HOST, PORT))# je lie mon socket au bon canal

except socket.error:
  print("La liaison du socket à l'adresse choisie a échoué.")
  sys.exit()
print("Serveur prêt, en attente de requêtes ...")
mySocket.listen(5)
 
# Attente et prise en charge des connexions demandées par les clients :
conn_client = {}	# dictionnaire des connexions clients
conn_pseudo = {}        # dictionnaire des pseudos
while 1:
  connexion, adresse = mySocket.accept()
  # Créer un nouvel objet thread pour gérer la connexion :
  th = ThreadClient(connexion)
  th.start()
  # Mémoriser la connexion dans le dictionnaire :
  it = th.getName()	  # identifiant du thread
  conn_client[it] = connexion
  conn_pseudo[it] = ""
  print("Client %s connecté, adresse IP %s, port %s." %\
     (it, adresse[0], adresse[1]))
  # Dialogue avec le client :
  msg ="Vous êtes connecté. Entrer votre pseudo."
  connexion.send(msg.encode("Utf8"))
  
