import socket
import threading

IP = "127.0.0.1"
PORT = 55555

class ChatServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((IP, PORT))
        self.server.listen(10)
        self.clients = {}  # {socket: pseudo}
        print("Serveur démarré sur", IP, ":", PORT)

    def broadcast(self, message, sender_socket=None):
        for client_socket in self.clients:
            if client_socket != sender_socket:  # Ne pas renvoyer au sender
                try:
                    client_socket.send(message.encode())
                except:
                    self.remove_client(client_socket)

    def handle_client(self, client_socket):
        try:
            # Recevoir le pseudo
            pseudo = client_socket.recv(1024).decode()
            self.clients[client_socket] = pseudo
            print(f"{pseudo} s'est connecté")
            
            # Annoncer la connexion
            self.broadcast(f"Système: {pseudo} a rejoint le chat")

            # Boucle principale de réception des messages
            while True:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                print(f"{pseudo}: {message}")
                self.broadcast(f"{pseudo}: {message}", client_socket)

        except Exception as e:
            print(f"Erreur avec {self.clients.get(client_socket, 'Unknown')}: {str(e)}")
        finally:
            self.remove_client(client_socket)

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            pseudo = self.clients[client_socket]
            print(f"{pseudo} s'est déconnecté")
            self.broadcast(f"Système: {pseudo} a quitté le chat")
            del self.clients[client_socket]
            client_socket.close()

    def start(self):
        print("En attente de connexions...")
        while True:
            client_socket, address = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.daemon = True
            thread.start()

def start():
    server = ChatServer()
    server.start()

if __name__ == "__main__":
    start()