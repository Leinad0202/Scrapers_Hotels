# Projeto: Booking + Hotels.com Scraper

## Descrição:
-----------
Este projeto automatiza a coleta de dados de hotéis para destinos específicos usando duas abordagens:
1. Booking.com via Selenium (navegação e scraping de páginas).
2. Hotels.com via API (com tentativa de descoberta automática da API interna).

## Objetivo:
-----------
- Coletar informações de hotéis (nome, preço, endereço, avaliações etc.) para análises, pesquisas ou aplicações pessoais.
- Testar estratégias de scraping robustas frente a bloqueios ou mudanças em sites.

## Estrutura do Projeto:
---------------------
app/

│

├── main.py                # Script principal para rodar o scraping

├── utils.py               # Funções auxiliares, como salvar JSON

├── scrapers/

│   ├── booking.py         # Lógica de scraping do Booking.com via Selenium

│   ├── hotels.py          # Scraper do Hotels.com via API

│   ├── api_probe.py       # Testa se a API do Hotels.com está acessível

│   ├── api_discovery.py   # Descobre a API do Hotels.com em tempo real

│   └── config.py          # Configurações e constantes (URLs, headers, payloads)

└── data/                  # Pasta para salvar resultados e screenshots

## Dependências:
--------------
- Python 3.14+
- Selenium
- Docker (para rodar containers standalone com Firefox)
- Requests
- Firefox (via container Selenium)

## Setup Inicial:
---------------
1. Clone o repositório:
   git clone <seu_repositorio_url>
2. Entre na pasta do projeto:
   cd Booking_Scraping
3. Construa a imagem Docker:
   docker compose build
4. Instale dependências (opcional se rodar dentro do container):
   pip install -r requirements.txt

## Uso:
-----
Para rodar o scraping, execute o comando abaixo dentro do projeto:

### Scraping para a cidade "Roma"

```bash
docker compose down --volumes --remove-orphans
docker compose build --no-cache
docker compose run scraper Roma
```

##Resultados:
------------
- Dados finais serão salvos em `app/data/results.json`.
- Screenshots de captchas ou bloqueios serão salvos em `app/data/`.

##Notas:
-------
- Booking.com é raspado via Selenium, por isso o processo é mais lento, mas confiável.
- Hotels.com usa uma API interna que pode mudar ou bloquear bots. O projeto tenta descobrir a API, mas bloqueios ou mudanças podem impedir o scraping.
- Para desenvolvimento futuro: integrar `api_probe` e `api_discovery` de forma mais robusta para lidar com mudanças na API do Hotels.com.
- Variável `ENABLE_HOTELS` em `config.py` permite ativar ou desativar o scraping do Hotels.com.

###Licença:
---------
Uso pessoal. Modifique e adapte como desejar. Não se responsabiliza por uso comercial ou violação de termos de sites.
