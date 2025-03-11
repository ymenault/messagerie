import socket
import threading

IP = "127.0.0.1"
PORT = 55555

class ChatServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((IP, PORT))
        self.server.listen(10)
        self.clients = set()  # Ensemble de sockets clients
        print("Serveur démarré sur", IP, ":", PORT)

    def broadcast(self, message, sender_socket=None):
        """Transmet le message à tous les clients sauf l'expéditeur"""
        for client_socket in self.clients:
            if client_socket != sender_socket:
                try:
                    # Envoyer le message tel quel, sans le modifier
                    client_socket.send(message)
                except:
                    self.remove_client(client_socket)

    def handle_client(self, client_socket):
        """Gère la connexion d'un client"""
        try:
            self.clients.add(client_socket)
            # Boucle principale de réception des messages
            while True:
                message = client_socket.recv(1024)
                if not message:
                    break
                # Transmettre le message tel quel, sans le décoder ni le modifier
                self.broadcast(message, client_socket)
        except Exception as e:
            print(f"Erreur avec un client: {str(e)}")
        finally:
            self.remove_client(client_socket)

    def remove_client(self, client_socket):
        """Retire un client de la liste et ferme sa connexion"""
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            client_socket.close()

    def start(self):
        print("En attente de connexions...")
        while True:
            client_socket, address = self.server.accept()
            print(f"Nouvelle connexion de {address}")
            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.daemon = True
            thread.start()

def start():
    server = ChatServer()
    server.start()

if __name__ == "__main__":
    start()