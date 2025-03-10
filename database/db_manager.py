import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_file="messages.db"):
        # Assurer que le dossier database existe
        os.makedirs(os.path.dirname(os.path.abspath(db_file)), exist_ok=True)
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        """Initialise la base de données avec les tables nécessaires."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Table des utilisateurs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    public_key TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table des messages
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER,
                    message TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sender_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()

    def add_user(self, username, public_key=None):
        """Ajoute un nouvel utilisateur."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (username, public_key) VALUES (?, ?)',
                    (username, public_key)
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Si l'utilisateur existe déjà, on récupère son ID
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
                result = cursor.fetchone()
                return result[0] if result else None

    def save_message(self, sender_username, message):
        """Enregistre un message dans la base de données."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            # Obtenir l'ID de l'utilisateur
            cursor.execute('SELECT id FROM users WHERE username = ?', (sender_username,))
            result = cursor.fetchone()
            if result:
                sender_id = result[0]
                cursor.execute(
                    'INSERT INTO messages (sender_id, message) VALUES (?, ?)',
                    (sender_id, message)
                )
                return True
            return False

    def get_recent_messages(self, limit=50):
        """Récupère les messages les plus récents."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT users.username, messages.message, messages.timestamp
                FROM messages
                JOIN users ON messages.sender_id = users.id
                ORDER BY messages.timestamp DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()

    def get_user_messages(self, username, limit=50):
        """Récupère les messages d'un utilisateur spécifique."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT messages.message, messages.timestamp
                FROM messages
                JOIN users ON messages.sender_id = users.id
                WHERE users.username = ?
                ORDER BY messages.timestamp DESC
                LIMIT ?
            ''', (username, limit))
            return cursor.fetchall()
