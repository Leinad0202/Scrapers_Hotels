from dataclasses import dataclass
from typing import Optional

@dataclass
class HotelResult:
    source: str
    name: Optional[str]
    location: Optional[str]
    price_amount: Optional[float]
    price_currency: Optional[str]
    rating: Optional[float]
    reviews_count: Optional[int]
    url: Optional[str]
    scraped_at: str

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "name": self.name,
            "location": self.location,
            "price_amount": self.price_amount,
            "price_currency": self.price_currency,
            "rating": self.rating,
            "reviews_count": self.reviews_count,
            "url": self.url,
            "scraped_at": self.scraped_at,
        }
