import random
import time
import requests

PROXIES = [
    # exemplos — substitua por proxies reais
    # "http://user:pass@ip:porta",
]

def human_delay(min_s=2.5, max_s=6.5):
    time.sleep(random.uniform(min_s, max_s))


def post_with_retry(
    url: str,
    headers: dict,
    json_payload: dict,
    max_retries: int = 3,
    timeout: int = 30
):
    for attempt in range(1, max_retries + 1):
        proxy = random.choice(PROXIES) if PROXIES else None

        try:
            response = requests.post(
                url,
                headers=headers,
                json=json_payload,
                timeout=timeout,
                proxies={"http": proxy, "https": proxy} if proxy else None
            )

            if response.status_code == 429:
                print(f"429 detectado (tentativa {attempt})")
                human_delay(10, 20)
                continue

            response.raise_for_status()
            return response

        except requests.RequestException as e:
            print(f"Erro na tentativa {attempt}: {e}")
            human_delay(5, 12)

    raise RuntimeError("API bloqueada após várias tentativas")
