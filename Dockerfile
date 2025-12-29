# Base: Selenium com Firefox já configurado
FROM selenium/standalone-firefox:latest

# Fica root para instalar dependências Python
USER root

WORKDIR /app

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Volta pro usuário padrão do Selenium
USER seluser

# Define variável de ambiente para Python
ENV PYTHONUNBUFFERED=1

# Garante que o Firefox rode headless mesmo se algum código esquecer de setar
ENV MOZ_HEADLESS=1

# Entry point para rodar o main.py como módulo
ENTRYPOINT ["python", "-m", "app.main"]
