from decimal import Decimal
from pydantic import BaseModel, field_validator

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

class Book(BaseModel):
    title: str
    price: Decimal
    rating: int
    availability: bool
    url: str
    upc: str | None = None
    description: str | None = None
    ai_insights: dict | None = None

    @field_validator("rating")
    @classmethod
    def rating_in_range(cls, v: int) -> int:
        if not 1 <= v <= 5:
            raise ValueError(f"Rating must be 1-5, got {v}")
        return v

    @field_validator("price", mode="before")
    @classmethod
    def strip_currency(cls, v: str | Decimal) -> str | Decimal:
        if isinstance(v, str):
            return v.lstrip("£$€").strip()
        return v

    def to_csv_row(self) -> dict:
        return {
            "title": self.title,
            "price": str(self.price),
            "rating": self.rating,
            "availability": self.availability,
            "url": self.url,
            "upc": self.upc or "",
            "description": (self.description or "").replace("\n", " "),
        }

class ScraperResult(BaseModel):
    total_books: int
    total_pages: int
    books: list[Book]