import socketio
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox, ttk
import threading
import mysql.connector
import hashlib
import queue
from PIL import Image, ImageTk
import os

class UserDatabase:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='wishzapp_user',  
                password='db123',  
                database='wishzapp_db'
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as e:
            messagebox.showerror("Erreur de base de données", str(e))
            raise

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_user(self, username, password):
        hashed_password = self.hash_password(password)
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, hashed_password))
        return self.cursor.fetchone()

    def get_users(self, current_user_id):
        query = "SELECT id, username FROM users WHERE id != %s"
        self.cursor.execute(query, (current_user_id,))
        return self.cursor.fetchall()

    def get_or_create_conversation(self, user1_id, user2_id):
        try:
            # Essayer de trouver une conversation existante
            query = """
            SELECT id FROM conversations 
            WHERE (user1_id = %s AND user2_id = %s) 
               OR (user1_id = %s AND user2_id = %s)
            """
            self.cursor.execute(query, (user1_id, user2_id, user2_id, user1_id))
            conversation = self.cursor.fetchone()

            if not conversation:
                # Créer une nouvelle conversation
                create_query = """
                INSERT INTO conversations (user1_id, user2_id) 
                VALUES (%s, %s)
                """
                self.cursor.execute(create_query, (user1_id, user2_id))
                self.connection.commit()
                conversation_id = self.cursor.lastrowid
                return conversation_id
            
            return conversation['id']
        except mysql.connector.Error as e:
            messagebox.showerror("Erreur de base de données", str(e))
            return None

    def get_conversation_messages(self, conversation_id):
        query = """
        SELECT m.message, u.username, m.sent_at 
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.conversation_id = %s
        ORDER BY m.sent_at
        """
        self.cursor.execute(query, (conversation_id,))
        return self.cursor.fetchall()

    def register_user(self, username, password, email=None):
        try:
            # Vérifier si l'utilisateur existe déjà
            check_query = "SELECT * FROM users WHERE username = %s"
            self.cursor.execute(check_query, (username,))
            if self.cursor.fetchone():
                messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà")
                return False
            
            # Hacher le mot de passe
            hashed_password = self.hash_password(password)
            
            # Requête d'insertion
            insert_query = """
            INSERT INTO users (username, password, email, created_at) 
            VALUES (%s, %s, %s, NOW())
            """
            
            # Exécuter la requête
            self.cursor.execute(insert_query, (username, hashed_password, email))
            self.connection.commit()
            
            messagebox.showinfo("Succès", "Utilisateur enregistré avec succès")
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Erreur de base de données", str(e))
            self.connection.rollback()
            return False

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

class StyledWindow:
    def __init__(self, title="Wishzapp", geometry="400x600", icon_path=None, logo_path=None):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        
        # Configurer l'icône de la fenêtre
        if icon_path and os.path.exists(icon_path):
            self.root.iconphoto(True, tk.PhotoImage(file=icon_path))
        
        # Style de la fenêtre
        self.root.configure(bg='#f0f0f0')
        
        # Logo (optionnel)
        if logo_path and os.path.exists(logo_path):
            self.add_logo(logo_path)
    
    def add_logo(self, logo_path, max_width=300):
        # Charger et redimensionner le logo
        logo_image = Image.open(logo_path)
        width, height = logo_image.size
        aspect_ratio = width / height
        new_height = 100
        new_width = int(new_height * aspect_ratio)
        
        logo_image = logo_image.resize((new_width, new_height), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(logo_image)
        
        # Créer un label pour le logo
        logo_label = tk.Label(self.root, image=self.logo, bg='#f0f0f0')
        logo_label.pack(pady=10)

class LoginWindow(StyledWindow):
    def __init__(self):
        # Chemins des fichiers
        base_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, 'assets', 'icon.jpg')
        logo_path = os.path.join(base_path, 'assets', 'logo.jpg')
        
        # Initialiser avec style
        super().__init__(title="Connexion Wishzapp", icon_path=icon_path, logo_path=logo_path)
        
        # Base de données utilisateurs
        self.db = UserDatabase()
        
        # Titre
        title_label = tk.Label(
            self.root, 
            text="Connexion Chat", 
            font=("Arial", 16, "bold"), 
            bg='#f0f0f0', 
            fg='#333333'
        )
        title_label.pack(pady=10)
        
        # Frame de connexion
        login_frame = tk.Frame(self.root, bg='#f0f0f0')
        login_frame.pack(padx=20, pady=10, fill='x')
        
        # Nom d'utilisateur
        username_label = tk.Label(login_frame, text="Nom d'utilisateur :", bg='#f0f0f0')
        username_label.pack(anchor='w')
        self.username_entry = tk.Entry(login_frame, width=30, font=('Arial', 10))
        self.username_entry.pack(pady=5, fill='x')
        
        # Mot de passe
        password_label = tk.Label(login_frame, text="Mot de passe :", bg='#f0f0f0')
        password_label.pack(anchor='w')
        self.password_entry = tk.Entry(login_frame, show="*", width=30, font=('Arial', 10))
        self.password_entry.pack(pady=5, fill='x')
        
        # Bouton de connexion
        login_button = tk.Button(
            login_frame, 
            text="Connexion", 
            command=self.login,
            bg='#4CAF50',  # Vert
            fg='white',
            font=('Arial', 10, 'bold')
        )
        login_button.pack(pady=10, fill='x')
        
        # Lier la touche Entrée à la connexion
        self.password_entry.bind('<Return>', lambda event: self.login())

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        user = self.db.validate_user(username, password)
        if user:
            # Fermer la fenêtre de login
            self.root.destroy()
            
            # Lancer la fenêtre de chat
            ChatClient(username, user['id'])
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")
    
    def run(self):
        self.root.mainloop()

class RegistrationWindow(StyledWindow):
    def __init__(self):
        # Chemins des fichiers
        base_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, 'assets', 'icon.jpg')
        logo_path = os.path.join(base_path, 'assets', 'logo.jpg')
        
        # Initialiser avec style
        super().__init__(title="Inscription Wishzapp", icon_path=icon_path, logo_path=logo_path)
        
        # Base de données utilisateurs
        self.db = UserDatabase()
        
        # Titre
        title_label = tk.Label(
            self.root, 
            text="Inscription Chat", 
            font=("Arial", 16, "bold"), 
            bg='#f0f0f0', 
            fg='#333333'
        )
        title_label.pack(pady=10)
        
        # Frame d'inscription
        register_frame = tk.Frame(self.root, bg='#f0f0f0')
        register_frame.pack(padx=20, pady=10, fill='x')
        
        # Champs d'inscription avec style
        fields = [
            ("Nom d'utilisateur :", "username", False),
            ("Mot de passe :", "password", True),
            ("Confirmer le mot de passe :", "confirm_password", True),
            ("Email (optionnel) :", "email", False)
        ]
        
        self.entries = {}
        for label_text, key, is_password in fields:
            label = tk.Label(register_frame, text=label_text, bg='#f0f0f0')
            label.pack(anchor='w')
            
            entry_type = tk.Entry if not is_password else lambda *args, **kwargs: tk.Entry(*args, show="*", **kwargs)
            entry = entry_type(register_frame, width=30, font=('Arial', 10))
            entry.pack(pady=5, fill='x')
            
            self.entries[key] = entry
        
        # Bouton d'inscription
        register_button = tk.Button(
            register_frame, 
            text="S'inscrire", 
            command=self.register,
            bg='#2196F3',  # Bleu
            fg='white',
            font=('Arial', 10, 'bold')
        )
        register_button.pack(pady=10, fill='x')

    def register(self):
        username = self.entries['username'].get().strip()
        password = self.entries['password'].get()
        confirm_password = self.entries['confirm_password'].get()
        email = self.entries['email'].get().strip() or None
        
        # Validation des champs
        if not username:
            messagebox.showerror("Erreur", "Nom d'utilisateur requis")
            return
        
        if not password:
            messagebox.showerror("Erreur", "Mot de passe requis")
            return
        
        if password != confirm_password:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
            return
        
        # Tentative d'inscription
        if self.db.register_user(username, password, email):
            self.root.destroy()
            # Lancer la fenêtre de login ou de chat
            LoginWindow()
    
    def run(self):
        self.root.mainloop()

class ChatClient:
    def __init__(self, username, user_id):
        # Base de données
        self.db = UserDatabase()
        
        # File d'attente pour les messages
        self.message_queue = queue.Queue()
        
        # Initialiser SocketIO
        self.sio = socketio.Client()
        
        # Stocker l'ID utilisateur
        self.user_id = user_id
        
        # Créer la fenêtre principale avec un style personnalisé
        self.root = tk.Tk()
        self.root.title(f"Wishzapp - {username}")
        self.root.geometry("1000x700")
        
        # Chemins des fichiers
        base_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, 'assets', 'icon.jpg')
        logo_path = os.path.join(base_path, 'assets', 'logo.jpg')
        
        # Configurer l'icône
        if os.path.exists(icon_path):
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((32, 32), Image.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(True, icon_photo)
        
        # Définir un dégradé de couleurs
        self.configure_gradient_background()
        
        # Stocker le nom d'utilisateur
        self.username = username
        
        # Conversation actuelle
        self.current_conversation_id = None
        
        # Configurer l'interface
        self.create_gui()
        
        # Connecter au serveur
        self.connect_to_server()
        
        # Démarrer le traitement des messages
        self.root.after(100, self.process_message_queue)
    
    def configure_gradient_background(self):
        # Créer un canvas pour le dégradé
        self.gradient_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.gradient_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Définir les couleurs du dégradé (bleu vers gris)
        self.create_gradient(
            start_color='#4A90E2',  # Bleu clair
            end_color='#E0E0E0'     # Gris clair
        )
    
    def create_gradient(self, start_color, end_color):
        def rgb_to_hex(r, g, b):
            return f'#{r:02x}{g:02x}{b:02x}'
        
        def interpolate_color(color1, color2, factor):
            # Convertir les couleurs hex en RGB
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            
            # Interpoler
            r = int(r1 + factor * (r2 - r1))
            g = int(g1 + factor * (g2 - g1))
            b = int(b1 + factor * (b2 - b1))
            
            return rgb_to_hex(r, g, b)
        
        # Créer un dégradé vertical
        for i in range(100):
            color = interpolate_color(start_color, end_color, i/100)
            self.gradient_canvas.create_line(
                0, i, self.root.winfo_screenwidth(), i, 
                fill=color
            )
    
    def create_gui(self):
        # Couleurs
        bg_gray = '#E6E6E6'  # Gris clair
        text_blue = '#4A90E2'  # Bleu principal
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=bg_gray)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame des utilisateurs à gauche
        users_frame = tk.Frame(main_frame, bg=bg_gray, relief=tk.RAISED, borderwidth=2)
        users_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), pady=10)
        
        # Label des utilisateurs
        users_title = tk.Label(
            users_frame, 
            text="Conversations", 
            font=("Arial", 14, "bold"), 
            bg=bg_gray, 
            fg=text_blue
        )
        users_title.pack(pady=10)
        
        # Liste des utilisateurs
        self.users_listbox = tk.Listbox(
            users_frame, 
            width=25, 
            font=('Arial', 10),
            bg=bg_gray,  
            fg=text_blue,  
            selectbackground=text_blue,  
            selectforeground='white'
        )
        self.users_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.users_listbox.bind('<<ListboxSelect>>', self.on_user_select)
        
        # Charger les utilisateurs
        self.load_users()
        
        # Frame de droite pour les messages
        messages_frame = tk.Frame(main_frame, bg=bg_gray)
        messages_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Titre de la conversation
        self.conversation_title = tk.Label(
            messages_frame, 
            text="Sélectionnez une conversation", 
            font=("Arial", 16, "bold"), 
            bg=bg_gray, 
            fg=text_blue
        )
        self.conversation_title.pack(pady=10)
        
        # Zone de messages
        self.messages_area = scrolledtext.ScrolledText(
            messages_frame, 
            wrap=tk.WORD, 
            width=60, 
            height=20,
            font=('Arial', 10),
            bg=bg_gray,  
            fg=text_blue,  
            insertbackground=text_blue
        )
        self.messages_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.messages_area.config(state=tk.DISABLED)
        
        # Cadre pour l'envoi de messages
        send_frame = tk.Frame(messages_frame, bg=bg_gray)
        send_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # Champ de saisie
        self.message_entry = tk.Entry(
            send_frame, 
            width=40, 
            font=('Arial', 12),
            bg=bg_gray,  
            fg=text_blue,  
            insertbackground=text_blue
        )
        self.message_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,10))
        
        # Bouton d'envoi
        send_button = tk.Button(
            send_frame, 
            text="Envoyer", 
            command=self.send_message,
            bg=text_blue,  
            fg='white',  
            font=('Arial', 10, 'bold')
        )
        send_button.pack(side=tk.RIGHT)
        
        # Lier la touche Entrée à l'envoi de message
        self.message_entry.bind('<Return>', lambda event: self.send_message())
    
    def load_users(self):
        users = self.db.get_users(self.user_id)
        for user in users:
            self.users_listbox.insert(tk.END, user['username'])
    
    def on_user_select(self, event):
        if not self.users_listbox.curselection():
            return
        
        selected_username = self.users_listbox.get(self.users_listbox.curselection())
        
        # Trouver l'ID de l'utilisateur sélectionné
        query = "SELECT id FROM users WHERE username = %s"
        self.db.cursor.execute(query, (selected_username,))
        selected_user = self.db.cursor.fetchone()
        
        if selected_user:
            # Créer ou récupérer la conversation
            self.current_conversation_id = self.db.get_or_create_conversation(
                self.user_id, 
                selected_user['id']
            )
            
            # Mettre à jour le titre de la conversation
            self.conversation_title.config(text=f"Conversation avec {selected_username}")
            
            # Charger l'historique des messages
            messages = self.db.get_conversation_messages(self.current_conversation_id)
            
            # Effacer les messages précédents
            self.messages_area.config(state=tk.NORMAL)
            self.messages_area.delete('1.0', tk.END)
            
            # Afficher l'historique des messages
            for msg in messages:
                formatted_msg = f"{msg['username']}: {msg['message']} ({msg['sent_at']})\n"
                self.messages_area.insert(tk.END, formatted_msg)
            
            self.messages_area.config(state=tk.DISABLED)
            self.messages_area.see(tk.END)
    
    def setup_socketio_events(self):
        @self.sio.on('connect')
        def on_connect():
            print(f'Connexion établie pour {self.username}')
        
        @self.sio.on('new_message')
        def on_message(data):
            self.message_queue.put(data)
        
        @self.sio.on('older_messages')
        def on_older_messages(data):
            self.display_older_messages(data)
        
        @self.sio.on('disconnect')
        def on_disconnect():
            self.message_queue.put("🔴 Déconnecté du serveur")
    
    def process_message_queue(self):
        try:
            while not self.message_queue.empty():
                message = self.message_queue.get_nowait()
                self.display_message(message)
        except queue.Empty:
            pass
        
        # Continuer à vérifier la file d'attente
        self.root.after(100, self.process_message_queue)
    
    def connect_to_server(self):
        try:
            self.sio.connect('http://localhost:5000')
            
            # Configurer les événements SocketIO
            self.setup_socketio_events()
            
            # Démarrer un thread pour gérer la connexion
            connection_thread = threading.Thread(target=self.sio.wait)
            connection_thread.daemon = True
            connection_thread.start()
        except Exception as e:
            messagebox.showerror("Erreur de connexion", str(e))
            self.root.quit()
    
    def send_message(self):
        message = self.message_entry.get().strip()
        if message and self.current_conversation_id:
            try:
                self.sio.emit('message', {
                    'conversation_id': self.current_conversation_id,
                    'sender_id': self.user_id,
                    'username': self.username, 
                    'message': message
                })
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Erreur d'envoi", str(e))
    
    def display_message(self, message):
        # Vérifier si le message est pour la conversation actuelle
        if (self.current_conversation_id and 
            message.get('conversation_id') == self.current_conversation_id):
            
            self.messages_area.config(state=tk.NORMAL)
            formatted_msg = f"{message['username']}: {message['message']}\n"
            self.messages_area.insert(tk.END, formatted_msg)
            self.messages_area.config(state=tk.DISABLED)
            self.messages_area.see(tk.END)
    
    def display_older_messages(self, messages):
        # Afficher les anciens messages au début de la zone de messages
        self.messages_area.config(state=tk.NORMAL)
        
        # Insérer les anciens messages au début
        for msg in reversed(messages):
            formatted_msg = f"{msg['username']}: {msg['message']} ({msg['sent_at']})\n"
            self.messages_area.insert('1.0', formatted_msg)
        
        self.messages_area.config(state=tk.DISABLED)
    
    def run(self):
        self.root.mainloop()
        self.sio.disconnect()

def main():
    root = tk.Tk()
    root.title("Wishzapp Chat")
    
    # Chemins des fichiers
    base_path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_path, 'assets', 'icon.jpg')
    logo_path = os.path.join(base_path, 'assets', 'logo.jpg')
    
    # Configurer l'icône
    if os.path.exists(icon_path):
        root.iconphoto(True, tk.PhotoImage(file=icon_path))
    
    root.geometry("300x400")
    root.configure(bg='#f0f0f0')
    
    # Logo
    if os.path.exists(logo_path):
        logo_image = Image.open(logo_path)
        width, height = logo_image.size
        aspect_ratio = width / height
        new_height = 150
        new_width = int(new_height * aspect_ratio)
        
        logo_image = logo_image.resize((new_width, new_height), Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo_image)
        
        logo_label = tk.Label(root, image=logo, bg='#f0f0f0')
        logo_label.image = logo  # Garder une référence
        logo_label.pack(pady=20)
    
    # Bouton de connexion
    login_button = tk.Button(
        root, 
        text="Connexion", 
        command=lambda: [root.destroy(), LoginWindow()],
        bg='#4CAF50',  # Vert
        fg='white',
        font=('Arial', 12, 'bold'),
        width=20
    )
    login_button.pack(pady=10)
    
    # Bouton d'inscription
    register_button = tk.Button(
        root, 
        text="S'inscrire", 
        command=lambda: [root.destroy(), RegistrationWindow()],
        bg='#2196F3',  # Bleu
        fg='white',
        font=('Arial', 12, 'bold'),
        width=20
    )
    register_button.pack(pady=10)
    
    root.mainloop()

if __name__ == '__main__':
    main()