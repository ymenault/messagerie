from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import mysql.connector

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class DatabaseManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='wishzapp_user',
            password='db123',
            database='wishzapp_db'
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def save_message(self, conversation_id, sender_id, message):
        try:
            query = """
            INSERT INTO messages (conversation_id, sender_id, message) 
            VALUES (%s, %s, %s)
            """
            self.cursor.execute(query, (conversation_id, sender_id, message))
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Erreur lors de l'enregistrement du message : {e}")

    def get_conversation_messages(self, conversation_id, limit=50):
        try:
            query = """
            SELECT m.id, m.message, u.username, m.sent_at 
            FROM messages m 
            JOIN users u ON m.sender_id = u.id 
            WHERE m.conversation_id = %s
            ORDER BY m.sent_at DESC 
            LIMIT %s
            """
            self.cursor.execute(query, (conversation_id, limit))
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Erreur lors de la récupération des messages : {e}")
            return []

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

db_manager = DatabaseManager()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connecté')

@socketio.on('message')
def handle_message(data):
    try:
        # Enregistrer le message dans la base de données
        db_manager.save_message(
            data['conversation_id'], 
            data['sender_id'], 
            data['message']
        )
        
        # Émettre le message à tous les clients connectés
        emit('new_message', data, broadcast=True)
    except Exception as e:
        print(f"Erreur lors du traitement du message : {e}")

@socketio.on('get_older_messages')
def handle_get_older_messages(data):
    try:
        conversation_id = data.get('conversation_id')
        limit = data.get('limit', 50)
        
        # Récupérer les anciens messages
        older_messages = db_manager.get_conversation_messages(conversation_id, limit)
        
        # Émettre les anciens messages uniquement à l'expéditeur
        emit('older_messages', older_messages)
    except Exception as e:
        print(f"Erreur lors de la récupération des anciens messages : {e}")

@socketio.on('disconnect')
def handle_disconnect():
    print('Client déconnecté')

if __name__ == '__main__':
    try:
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Erreur lors du démarrage du serveur : {e}")
    finally:
        db_manager.close()