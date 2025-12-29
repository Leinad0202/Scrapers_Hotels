# app/scrapers/api_discovery.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def discover_hotels_api(driver, destination: str):
    """
    Descobre a API interna do Hotels.com antes do scraping.
    Retorna um dict com 'url' e 'headers' ou None se não conseguir detectar.
    """
    try:
        # Abrir a página do destino
        url = f"https://www.hotels.com/search.do?resolved-location=CITY:{destination}&q-destination={destination}"
        driver.get(url)
        
        # Espera algum elemento da lista de hotéis carregar (indica que a página iniciou as requisições)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.hotel"))
        )
        
        # Executa script JS para capturar requests XHR/Fetch
        api_data = driver.execute_script("""
            let calls = [];
            let open = XMLHttpRequest.prototype.open;
            XMLHttpRequest.prototype.open = function() {
                calls.push(this);
                return open.apply(this, arguments);
            };
            return calls.map(c => c._url || c.responseURL || null).filter(u => u && u.includes('graphql'));
        """)
        
        if api_data and len(api_data) > 0:
            # Retorna a primeira URL encontrada com 'graphql'
            api_url = api_data[0]
            headers = {
                "User-Agent": driver.execute_script("return navigator.userAgent;"),
                "Accept": "*/*",
                "Content-Type": "application/json",
            }
            return {"url": api_url, "headers": headers}
        else:
            return None
    except Exception as e:
        print(f"Erro ao descobrir API: {e}")
        return None
