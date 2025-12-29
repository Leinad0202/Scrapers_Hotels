from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta
from typing import List, Optional
from functools import wraps

import time
import random
import re
import logging
from urllib.parse import urlencode

from app.models.hotel import HotelResult


# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("booking_scraper")


# ---------------- UTILS ----------------
def random_sleep(a=0.8, b=1.6):
    time.sleep(a + random.random() * (b - a))


def retry(attempts=3, base_delay=1.0, jitter=0.5):
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    delay = base_delay * (2 ** i) + random.random() * jitter
                    logger.warning(f"{func.__name__} failed ({i+1}/{attempts}): {e}")
                    time.sleep(delay)
            raise last_exc
        return wrapper
    return deco


def normalize_text(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    return re.sub(r"\s+", " ", text).strip()


def parse_price(text: str):
    if not text:
        return None, None

    text = text.replace("\u00A0", " ").strip()
    m = re.search(r"([^\d.,-]*?)\s*([\d.,]+)", text)
    if not m:
        return None, None

    currency = m.group(1).strip() or None
    num = m.group(2)

    if "," in num and "." in num:
        num = num.replace(".", "").replace(",", ".")
    else:
        num = num.replace(",", ".")

    try:
        return float(num), currency
    except ValueError:
        return None, None


def build_search_url(destino: str, checkin=None, checkout=None):
    today = datetime.utcnow().date()
    checkin = checkin or (today + timedelta(days=1))
    checkout = checkout or (checkin + timedelta(days=1))

    params = {
        "ss": destino,
        "checkin_year": checkin.year,
        "checkin_month": checkin.month,
        "checkin_monthday": checkin.day,
        "checkout_year": checkout.year,
        "checkout_month": checkout.month,
        "checkout_monthday": checkout.day,
        "group_adults": 2,
        "no_rooms": 1,
        "group_children": 0,
        "selected_currency": "BRL",
        "order": "bayesian_review_score",  # MELHORES AVALIAÇÕES
        # "price_range": 1  # opcional, se quiser limitar faixa de preço baixa
    }

    return "https://www.booking.com/searchresults.html?" + urlencode(params)


@retry()
def open_driver(headless=True, user_agent=None):
    options = Options()
    if headless:
        options.add_argument("--headless")

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    if user_agent:
        options.set_preference("general.useragent.override", user_agent)

    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(3)
    return driver


# ---------------- SELECTORS ----------------
CARD_SELECTOR = '[data-testid="property-card"]'
TITLE_SELECTOR = '[data-testid="title"]'
ADDRESS_SELECTOR = '[data-testid="address"]'

PRICE_SELECTORS = [
    '[data-testid="price-and-discounted-price"]',
    '[data-testid="price"]',
    'span[class*="price"]'
]

RATING_SELECTOR = '[data-testid="review-score"]'


# ---------------- SCRAPER ----------------
def scrape_booking(
    driver,
    destino: str,
    paginas: int = 3,
    checkin=None,
    checkout=None,
    headless: bool = True,
    user_agent: Optional[str] = None
) -> List[HotelResult]:

    driver = None
    results: List[HotelResult] = []
    seen_urls = set()

    try:
        driver = open_driver(headless, user_agent)
        wait = WebDriverWait(driver, 30)

        url = build_search_url(destino, checkin, checkout)
        logger.info(f"Abrindo: {url}")
        driver.get(url)

        # cookies
        try:
            btn = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            btn.click()
        except Exception:
            pass

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, CARD_SELECTOR)))

        for page in range(paginas):
            logger.info(f"Página {page+1}")

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            random_sleep(0.5, 1.2)

            cards = driver.find_elements(By.CSS_SELECTOR, CARD_SELECTOR)

            for c in cards:
                try:
                    # -------- URL --------
                    try:
                        a = c.find_element(By.CSS_SELECTOR, "a")
                        hotel_url = a.get_attribute("href")
                        if hotel_url:
                            hotel_url = hotel_url.split("?")[0]
                    except:
                        continue

                    if not hotel_url or hotel_url in seen_urls:
                        continue

                    seen_urls.add(hotel_url)

                    # -------- DATA --------
                    name = normalize_text(
                        c.find_element(By.CSS_SELECTOR, TITLE_SELECTOR).text
                    )

                    location = normalize_text(
                        c.find_element(By.CSS_SELECTOR, ADDRESS_SELECTOR).text
                    )

                    price_amount, price_currency = None, None
                    for sel in PRICE_SELECTORS:
                        try:
                            price_text = c.find_element(By.CSS_SELECTOR, sel).text
                            price_amount, price_currency = parse_price(price_text)
                            if price_amount:
                                break
                        except:
                            continue

                    rating = None
                    try:
                        rating_text = c.find_element(By.CSS_SELECTOR, RATING_SELECTOR).text
                        m = re.search(r"([\d.,]+)", rating_text)
                        if m:
                            rating = float(m.group(1).replace(",", "."))
                    except:
                        pass

                    results.append(
                        HotelResult(
                            source="booking",
                            name=name,
                            location=location,
                            price_amount=price_amount,
                            price_currency=price_currency,
                            rating=rating,
                            reviews_count=None,
                            url=hotel_url,
                            scraped_at=datetime.utcnow().isoformat()
                        )
                    )

                except Exception as e:
                    logger.warning(f"Erro ao processar card: {e}")

            # -------- PAGINAÇÃO --------
            try:
                next_buttons = driver.find_elements(
                    By.CSS_SELECTOR,
                    'button[aria-label*="Next"], a[aria-label*="Next"], '
                    'button[aria-label*="Próxima"], a[aria-label*="Próxima"]'
                )

                for b in next_buttons:
                    if b.is_displayed() and b.is_enabled():
                        driver.execute_script("arguments[0].click();", b)
                        random_sleep(1, 2)
                        break
                else:
                    break

            except Exception:
                break

        return results

    finally:
        if driver:
            driver.quit()
