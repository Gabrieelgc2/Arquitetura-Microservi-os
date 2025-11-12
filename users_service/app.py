import json
from flask import Flask, jsonify, abort

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Dados de usuários fixos
USERS = {
    '1': {'id': 1, 'name': 'Alice Silva', 'email': 'alice@exemplo.com'},
    '2': {'id': 2, 'name': 'Bruno Santos', 'email': 'bruno@exemplo.com'},
    '3': {'id': 3, 'name': 'Carla Costa', 'email': 'carla@exemplo.com'}
}

@app.route('/users', methods=['GET'])
def get_users():
    """Retorna todos os usuários."""
    print("✅ [User Service] Requisição: GET /users")
    return jsonify(list(USERS.values()))

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retorna um usuário específico pelo ID."""
    print(f"✅ [User Service] Requisição: GET /users/{user_id}")
    user = USERS.get(user_id)
    if user:
        return jsonify(user)
    
    print(f"❌ [User Service] Usuário {user_id} não encontrado.")
    # Se o usuário não for encontrado, retornamos 404
    abort(404, description=f"Usuário com ID '{user_id}' não encontrado.")

if __name__ == '__main__':
    # Roda em 0.0.0.0 para ser acessível pelo Docker
    print("🚀 User Service iniciado na porta 5001...")
    app.run(host='0.0.0.0', port=5001)