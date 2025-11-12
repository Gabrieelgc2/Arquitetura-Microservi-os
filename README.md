🚀 Sistema de Microsserviços com Docker e API GatewayEste projeto implementa uma arquitetura simples de microsserviços usando Python (Flask), Docker para containerização e Docker Compose para orquestração. O sistema é composto por três serviços: User Service, Order Service e API Gateway.🏗️ Estrutura do Projeto/
├── gateway_service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── orders_service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── users_service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── docker-compose.yml
└── README.md
⚙️ Pré-requisitosVocê deve ter o Docker e o Docker Compose instalados em sua máquina.
🏃 Como Executar: Execute os seguintes comandos no diretório raiz do projeto:
1. Construir e Iniciar os Containers O comando abaixo irá construir as imagens Docker para cada serviço e iniciá-los, configurando a rede interna (microservice-net):docker-compose up --build
Observação: O parâmetro --build garante que as imagens sejam criadas ou atualizadas antes de subir os containers.
2. Verificar o StatusVocê deve ver logs de todos os três serviços (User, Order e Gateway) no seu terminal. O sistema estará pronto quando o log do api-gateway indicar que está rodando na porta 8080 (interna), que está mapeada para a porta 8888 do seu host.
🧪 Como TestarTodos os testes devem ser feitos através do API Gateway, que agora está exposto na porta 8888 do seu host.Teste 1: User Service (via Gateway)Endpoint: GET /api/userscurl http://localhost:8888/api/users
Resultado Esperado: Uma lista JSON de todos os usuários.
Teste 2: User Service Individual (via Gateway)Endpoint: GET /api/users/1curl http://localhost:8888/api/users/1
Resultado Esperado: Os dados do usuário com id: 1.
Teste 3: Order Service (com validação via Gateway)Endpoint: GET /api/orders/1curl http://localhost:8888/api/orders/1
Resultado Esperado: Uma lista de pedidos associados ao usuário 1. (Você deve ver no terminal do order-service a mensagem de requisição ao user-service).
Teste 4: Order Service (Usuário Inexistente)Endpoint: GET /api/orders/99curl http://localhost:8888/api/orders/99
Resultado Esperado: Um erro 404 Not Found (propagado do User Service, via Order Service, até o Gateway).🛑 Como PararPara parar e remover os containers:docker-compose down
