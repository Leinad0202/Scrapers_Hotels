from datetime import datetime
from app.scrapers.request_utils import post_with_retry, human_delay
from app.scrapers.config import HOTELS_GRAPHQL_URL, HOTELS_HEADERS, HOTELS_PAYLOAD
from app.models.hotel import HotelResult

def scrape_hotels_api(destination: str):
    payload = HOTELS_PAYLOAD(destination)
    results = []

    human_delay(4, 8)

    response = post_with_retry(
        HOTELS_GRAPHQL_URL,
        HOTELS_HEADERS,
        payload,
        max_retries=3
    )

    data = response.json()
    properties = (
        data.get("data", {})
        .get("propertySearch", {})
        .get("properties", [])
    )

    for hotel in properties:
        results.append(
            HotelResult(
                source="hotels",
                name=hotel.get("name"),
                location=destination,
                price_amount=hotel.get("price", {}).get("lead", {}).get("amount"),
                price_currency="BRL",
                rating=hotel.get("guestReviews", {}).get("score"),
                reviews_count=None,
                url=hotel.get("urls", {}).get("hotelPageUrl"),
                scraped_at=datetime.utcnow().isoformat()
            )
        )

        human_delay(0.3, 1.1)

    return results
