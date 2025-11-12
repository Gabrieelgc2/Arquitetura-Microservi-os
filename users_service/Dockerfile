# Usa uma imagem Python leve
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos e os instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app.py .

# Expõe a porta que o Flask vai usar (internamente)
EXPOSE 5001

# Comando para rodar a aplicação
CMD ["python", "app.py"]