import json
from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# URLs dos microsserviços na rede Docker
USER_SERVICE_URL = "http://user-service:5001"
ORDER_SERVICE_URL = "http://order-service:5002"

@app.errorhandler(503)
def service_unavailable(error):
    """Handler para erros 503 (Serviço Indisponível)."""
    return jsonify({
        'error': 'Service Unavailable', 
        'message': error.description
    }), 503

def forward_request(service_url):
    """Função genérica para encaminhar a requisição e retornar a resposta."""
    
    # Constrói a URL completa para o microsserviço
    # Usamos request.full_path para obter o path original da requisição externa
    target_path = request.full_path.replace('/api', '', 1) 
    target_url = f"{service_url}{target_path}"
    
    print(f"➡️ [Gateway] Encaminhando {request.method} {target_path} para: {target_url}")
    
    try:
        # Encaminha a requisição, mantendo o método e os dados (se houver)
        response = requests.request(
            method=request.method,
            url=target_url,
            headers={k: v for k, v in request.headers if k != 'Host'}, # Copia headers, exceto Host
            data=request.get_data(),
            timeout=10 # Adiciona um timeout simples para boas práticas
        )
        
        print(f"⬅️ [Gateway] Recebido status {response.status_code} do microsserviço.")
        
        # Retorna a resposta do microsserviço para o cliente externo
        return (response.content, response.status_code, response.headers.items())

    except requests.exceptions.ConnectionError:
        print(f"❌ [Gateway] Erro de Conexão: Microsserviço em {service_url} indisponível.")
        abort(503, description=f"O serviço em {service_url.split('//')[1]} está indisponível.")
    except Exception as e:
        print(f"❌ [Gateway] Erro inesperado: {e}")
        abort(500, description="Erro interno no Gateway ao processar a requisição.")


# Roteamento para User Service
# GET /api/users
@app.route('/api/users', defaults={'user_id': None}, methods=['GET'])
# GET /api/users/<id>
@app.route('/api/users/<user_id>', methods=['GET'])
def users_route(user_id):
    """Encaminha requisições de /api/users para o User Service."""
    return forward_request(USER_SERVICE_URL)

# Roteamento para Order Service
# GET /api/orders/<user_id>
@app.route('/api/orders/<user_id>', methods=['GET'])
def orders_route(user_id):
    """Encaminha requisições de /api/orders para o Order Service."""
    return forward_request(ORDER_SERVICE_URL)

if __name__ == '__main__':
    # Roda em 0.0.0.0 para ser acessível pelo Docker
    print("🚀 API Gateway iniciado na porta 8080...")
    app.run(host='0.0.0.0', port=8081)