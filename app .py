from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "database.db"

def init_db():
    """Inicializa o banco de dados SQLite com a tabela de jogadores."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            score INTEGER DEFAULT 0,
            headshots INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/players', methods=['GET'])
def get_players():
    """Retorna a lista de todos os jogadores cadastrados no banco de dados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, score, headshots FROM players ORDER BY score DESC")
    players = cursor.fetchall()
    conn.close()
    
    player_list = [
        {"id": p[0], "username": p[1], "score": p[2], "headshots": p[3]} 
        for p in players
    ]
    return jsonify(player_list)

@app.route('/api/players', methods=['POST'])
def add_player():
    """Adiciona um novo jogador ao banco de dados."""
    data = request.json
    username = data.get('username')
    score = data.get('score', 0)
    headshots = data.get('headshots', 0)

    if not username:
        return jsonify({"error": "O nome do jogador é obrigatório!"}), 400

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO players (username, score, headshots) VALUES (?, ?, ?)",
            (username, score, headshots)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Jogador adicionado com sucesso!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Nome de usuário já existe!"}), 400

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

