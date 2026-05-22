import csv
import json
import logging
from pathlib import Path
from scraper.models import Book, ScraperResult

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("output")

def save_results(result: ScraperResult, output_dir: Path = OUTPUT_DIR) -> None:
    """Salva os resultados em JSON e CSV no diretório de saída."""
    output_dir.mkdir(parents=True, exist_ok=True)
    _save_json(result, output_dir)
    _save_csv(result.books, output_dir)
    logger.info("Dados salvos em %s (JSON + CSV)", output_dir)

def _save_json(result: ScraperResult, output_dir: Path) -> None:
    path = output_dir / "books.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result.model_dump(mode="json"), f, ensure_ascii=False, indent=2)
    logger.info("JSON: %s (%d livros)", path, result.total_books)

def _save_csv(books: list[Book], output_dir: Path) -> None:
    path = output_dir / "books.csv"
    if not books:
        return

    # O ESTÁ AQUI ABAIXO:
    primeiro_livro = next(iter(books))
    fieldnames = list(primeiro_livro.to_csv_row().keys())
    
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(b.to_csv_row() for b in books)

    logger.info("CSV: %s (%d linhas)", path, len(books))