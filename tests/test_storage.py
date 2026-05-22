import json
from scraper.storage import save_results
from scraper.models import ScraperResult, Book

def test_save_results(tmp_path):
    book = Book(title="Mock", price="42.0", rating=5, availability=True, url="http://x")
    result = ScraperResult(total_books=1, total_pages=1, books=[book])

    save_results(result, output_dir=tmp_path)

    json_file = tmp_path / "books.json"
    csv_file = tmp_path / "books.csv"

    assert json_file.exists()
    assert csv_file.exists()

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["total_books"] == 1