import logging
from rich.progress import Progress, SpinnerColumn, TextColumn
from scraper.models import Book, ScraperResult
from scraper.storage import save_results
from scraper.crawler import run_playwright_scraper

logger = logging.getLogger(__name__)

async def run(
    max_pages: int | None = None, 
    delay: float = 0.5,
    category_url: str | None = None,
    use_ai: bool = False,
    search_title: str | None = None # NOVO PARÂMETRO
) -> ScraperResult:
    """Orquestra a extração e a validação de dados."""
    
    msg_extracao = "[bold blue]Executando Playwright RPA... Extraindo dados...[/bold blue]"
    if use_ai:
        msg_extracao = "[bold magenta]Executando Playwright RPA + Groq IA...[/bold magenta]"

    with Progress(
        SpinnerColumn(),
        TextColumn(msg_extracao),
    ) as progress:
        task = progress.add_task("Extraindo...", total=None)
        
        # Repassa todos os novos argumentos para o crawler
        books_data, total_pages = await run_playwright_scraper(
            max_pages=max_pages, 
            delay=delay,
            category_url=category_url,
            use_ai=use_ai,
            search_title=search_title 
        )
        progress.update(task, completed=100)

    books = []
    for d in books_data:
        try:
            books.append(Book(**d))
        except Exception as e:
            logger.warning("Livro inválido ignorado: %s | erro: %s", d.get("title"), e)

    result = ScraperResult(
        total_books=len(books),
        total_pages=total_pages,
        books=books,
    )

    save_results(result)
    return result