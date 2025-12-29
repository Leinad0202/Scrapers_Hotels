from app.scrapers.request_utils import post_with_retry, human_delay
from app.scrapers.config import HOTELS_GRAPHQL_URL, HOTELS_HEADERS, HOTELS_PAYLOAD

def probe_api(destination: str) -> bool:
    payload = HOTELS_PAYLOAD(destination)

    try:
        human_delay(3, 6)
        response = post_with_retry(
            HOTELS_GRAPHQL_URL,
            HOTELS_HEADERS,
            payload,
            max_retries=2
        )
        data = response.json()
        return "propertySearch" in str(data)
    except Exception as e:
        print(f"Probe falhou: {e}")
        return False
