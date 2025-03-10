import subprocess
import os
import tkinter as tk
import threading
import socket
import random
import sys
from pathlib import Path

# Ajouter le chemin pour les modules de chiffrement
sys.path.append(str(Path(__file__).parent / "messagerie-main"))
from chiffrement.AES import encrypt as aes_encrypt, decrypt as aes_decrypt
from chiffrement.RSA import encrypt as rsa_encrypt, decrypt as rsa_decrypt, load_keys

class MessagingApp:
    def __init__(self, master):
        self.master = master
        master.title("Messaging App")
        
        # Déterminer le type de serveur
        try:
            with open('server_type.txt', 'r') as file:
                self.server_type = file.read().strip()
        except FileNotFoundError:
            self.server_type = 'server'  # Type par défaut
            
        # Configuration du chiffrement RSA si nécessaire
        if self.server_type == 'server_rsa':
            self.priv_key, self.pub_key = load_keys()

        # Frame pour le pseudo
        self.pseudo_frame = tk.Frame(master)
        self.pseudo_frame.pack(pady=10)
        
        tk.Label(self.pseudo_frame, text="Pseudo:").pack(side=tk.LEFT)
        self.pseudo_entry = tk.Entry(self.pseudo_frame)
        self.pseudo_entry.pack(side=tk.LEFT, padx=5)
        self.pseudo = f"User_{random.randint(1000, 9999)}"
        self.pseudo_entry.insert(0, self.pseudo)
        self.pseudo_entry.config(state=tk.DISABLED)
        
        # Zone de chat
        self.text_area = tk.Text(master, height=20, width=50)
        self.text_area.pack(pady=10)
        self.text_area.config(state=tk.DISABLED)

        # Frame pour l'entrée de message
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(pady=5, fill=tk.X, padx=10)
        
        self.entry = tk.Entry(self.input_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind('<Return>', lambda e: self.send_message())

        self.send_button = tk.Button(self.input_frame, text="Envoyer", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=5)

        # Configuration de la socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def encrypt_message(self, message):
        if self.server_type == 'server_aes':
            return aes_encrypt(message)
        elif self.server_type == 'server_rsa':
            return rsa_encrypt(message, self.pub_key)
        return message

    def decrypt_message(self, message):
        if self.server_type == 'server_aes':
            return aes_decrypt(message)
        elif self.server_type == 'server_rsa':
            return rsa_decrypt(message, self.priv_key)
        return message

    def connect_to_server(self):
        try:
            self.socket.connect(('localhost', 55555))
            self.connected = True
            
            # Envoyer le pseudo selon le type de serveur
            if self.server_type in ['server_aes', 'server_rsa']:
                pseudo_encrypted = self.encrypt_message(self.pseudo)
                self.socket.send(pseudo_encrypted.encode() if isinstance(pseudo_encrypted, str) else pseudo_encrypted)
            else:
                self.socket.send(self.pseudo.encode())

            # Démarrer le thread de réception
            self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            self.receive_thread.start()
            self.add_message("Système", "Connecté au serveur!")
            return True
        except Exception as e:
            self.add_message("Système", f"Erreur de connexion: {str(e)}")
            return False

    def add_message(self, sender, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"{sender}: {message}\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def send_message(self):
        if not self.connected:
            if not self.connect_to_server():
                return

        message = self.entry.get().strip()
        if message:
            try:
                # Préparer le message avec le pseudo
                full_message = f"{self.pseudo}: {message}"
                
                # Chiffrer le message si nécessaire
                if self.server_type in ['server_aes', 'server_rsa']:
                    encrypted_message = self.encrypt_message(full_message)
                    self.socket.send(encrypted_message.encode() if isinstance(encrypted_message, str) else encrypted_message)
                else:
                    self.socket.send(full_message.encode())
                    
                self.add_message("Vous", message)
                self.entry.delete(0, tk.END)
            except Exception as e:
                self.add_message("Système", f"Erreur d'envoi: {str(e)}")
                self.connected = False

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(4096 if self.server_type == 'server_rsa' else 1024)
                if not data:
                    break
                    
                # Décrypter le message si nécessaire
                if self.server_type in ['server_aes', 'server_rsa']:
                    message = self.decrypt_message(data if self.server_type == 'server_rsa' else data.decode())
                else:
                    message = data.decode()

                if message:
                    # Ne pas afficher les messages provenant de nous-mêmes
                    if not message.startswith(f"{self.pseudo}:"):
                        sender, contenu = message.split(":", 1)
                        self.master.after(0, lambda s=sender.strip(), m=contenu.strip(): self.add_message(s, m))
            except Exception as e:
                print(f"Erreur de réception: {str(e)}")
                self.connected = False
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = MessagingApp(root)
    root.mainloop()