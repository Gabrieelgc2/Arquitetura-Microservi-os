import json
from flask import Flask, jsonify, abort
import requests

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# O hostname 'user-service' será resolvido pelo Docker Compose
USER_SERVICE_URL = "http://user-service:5001/users"

# Dados de pedidos fixos
ORDERS = {
    '1': [
        {'order_id': 'P001', 'item': 'Laptop', 'price': 1200.00},
        {'order_id': 'P002', 'item': 'Mouse Pad', 'price': 15.00}
    ],
    '2': [
        {'order_id': 'P003', 'item': 'Monitor 4K', 'price': 550.00}
    ],
    '3': [
        {'order_id': 'P004', 'item': 'Teclado Mecânico', 'price': 99.00},
        {'order_id': 'P005', 'item': 'Webcam HD', 'price': 45.00},
        {'order_id': 'P006', 'item': 'Microfone USB', 'price': 75.00}
    ]
}

@app.route('/orders/<user_id>', methods=['GET'])
def get_orders(user_id):
    """
    Retorna pedidos de um usuário após validar sua existência no User Service.
    """
    print(f"🔁 [Order Service] Requisição: GET /orders/{user_id}")
    
    # 1. Tenta validar o usuário no User Service
    user_validation_url = f"{USER_SERVICE_URL}/{user_id}"
    print(f"   - Requisitando dados do User Service em: {user_validation_url}")
    
    try:
        response = requests.get(user_validation_url)
        
        if response.status_code == 404:
            # Usuário não existe, retorna 404
            print(f"   - ❌ User Service retornou 404. Usuário {user_id} não encontrado.")
            abort(404, description=f"Usuário ID '{user_id}' não encontrado ou inválido.")

        response.raise_for_status() # Lança exceção para 5xx e 4xx (exceto 404 já tratada)
        
        user_data = response.json()
        print(f"   - ✅ User Service validado: {user_data['name']}")
        
        # 2. Retorna os pedidos
        user_orders = ORDERS.get(user_id, [])
        return jsonify({
            'user_id': user_id,
            'user_name': user_data['name'],
            'orders': user_orders
        })

    except requests.exceptions.ConnectionError:
        print("   - ❌ Erro de Conexão: User Service não está acessível.")
        abort(503, description="Serviço de Usuário (User Service) indisponível.")
    except Exception as e:
        print(f"   - ❌ Erro ao processar requisição: {e}")
        abort(500, description="Erro interno no Order Service.")


if __name__ == '__main__':
    # Roda em 0.0.0.0 para ser acessível pelo Docker
    print("🚀 Order Service iniciado na porta 5002...")
    app.run(host='0.0.0.0', port=5002)