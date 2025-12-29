import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from app.scrapers.config import ENABLE_HOTELS
from app.scrapers.booking import scrape_booking
from app.scrapers.hotels import scrape_hotels_api
from app.scrapers.api_discovery import discover_hotels_api
from app.utils import save_json


def create_firefox_driver(headless: bool = True):
    """Cria um Firefox driver dentro do container standalone Selenium."""
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Firefox(options=options)
    return driver


def main():
    if len(sys.argv) < 2:
        print('Uso: python -m app.main "Cidade"')
        return

    destino = sys.argv[1]
    resultados = []

    # Booking via Selenium
    driver = create_firefox_driver(headless=True)
    print(f"Iniciando scraping do Booking para: {destino}")
    resultados.extend(scrape_booking(driver, destino, paginas=3))
    driver.quit()

    # Hotels.com via scraping/API discovery
    if ENABLE_HOTELS:
        driver = create_firefox_driver(headless=True)
        print(f"Descobrindo API do Hotels.com para: {destino}...")
        api_info = discover_hotels_api(driver, destino)
        driver.quit()

        if api_info:
            print(f"API descoberta: {api_info['url']}")
            resultados.extend(scrape_hotels(destino, api_url=api_info["url"], headers=api_info["headers"]))
        else:
            print("Hotels.com bloqueado ou alterado, pulando scraping.")

    # Salvar resultados finais
    save_json(resultados, "/app/data/results.json")

    print("Finalizado!")
    print(f"{len(resultados)} resultados coletados.")


if __name__ == "__main__":
    main()
