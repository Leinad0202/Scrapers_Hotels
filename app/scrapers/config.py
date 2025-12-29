# config.py

# --- Hotels.com API padrão ---
HOTELS_GRAPHQL_URL = "https://www.hotels.com/api/graphql"

HOTELS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Accept": "*/*",
    "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
    "Content-Type": "application/json",
    "client-info": "shopping-pwa",
    "x-shopping-product-line": "lodging",
    "Origin": "https://www.hotels.com",
    "Referer": "https://www.hotels.com/"
}

def HOTELS_PAYLOAD(destination: str):
    return {
        "operationName": "PropertyListingQuery",
        "variables": {
            "criteria": {
                "primary": {
                    "destination": {"regionName": destination},
                    "rooms": [{"adults": 2}]
                }
            }
        }
    }

# --- Variáveis extras que o main.py espera ---
ENABLE_HOTELS = True  # ativa/desativa scraping do Hotels.com
HOTELS_HASH = "abc123"  # hash inicial do payload (pode ser atualizado dinamicamente pelo discovery)

# --- Timeout e limites para probe ---
HOTELS_PROBE_MAX_RETRIES = 3  # número de tentativas antes de considerar API bloqueada
HOTELS_PROBE_TIMEOUT = 5      # timeout em segundos por requisição
