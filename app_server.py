import importlib
import subprocess
import sys

# Installer les dépendances à partir de requirements.txt
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

# Demander à l'utilisateur de choisir le type de codage
print("Choisissez le type de serveur:")
print("1. Serveur de base")
print("2. Serveur AES")
print("3. Serveur RSA")
choice = input("Entrez votre choix (1/2/3): ")

if choice == '1':
    server_module = 'messagerie-main.servers.server'
elif choice == '2':
    server_module = 'messagerie-main.servers.server_aes'
elif choice == '3':
    server_module = 'messagerie-main.servers.server_rsa'
else:
    print("Choix invalide, utilisation du serveur de base par défaut.")
    server_module = 'server'

# Après avoir demandé à l'utilisateur de choisir le type de serveur
with open("server_type.txt", "w") as file:
    file.write(server_module.split('.')[-1])  # Écrit le type de serveur (ex: 'server_aes')

# Importer le module de serveur choisi
server = importlib.import_module(server_module)

# Démarrer le serveur
server.start()