import asyncio
import logging
import typer
from rich.logging import RichHandler
from scraper.pipeline import run as pipeline_run
from rich import print as rprint
from dotenv import load_dotenv

load_dotenv()
app = typer.Typer(help="Scraper assíncrono para books.toscrape.com")

def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

@app.command()
def run(
    max_pages: int = typer.Option(None, "--max-pages", "-p", help="Limite de páginas"),
    delay: float = typer.Option(0.5, "--delay", "-d", help="Delay entre requests"),
    use_ai: bool = typer.Option(False, "--ai", help="Ativar extração com Groq LLM"),
    category: str = typer.Option(None, "--category", "-c", help="Slug da categoria (ex: travel_2)"),
    search: str = typer.Option(None, "--search", "-s", help="Busca exata por parte do título"), # NOVO COMANDO
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Coleta os livros usando automação de navegador (Playwright) e salva em output/."""
    _setup_logging(verbose)

    category_url = None
    if category:
        category_url = f"https://books.toscrape.com/catalogue/category/books/{category}/index.html"
        rprint(f"[bold cyan]🔍 Focando na categoria: {category}[/bold cyan]")

    if search:
        rprint(f"[bold yellow]🔍 Buscando por: {search}[/bold yellow]")

    rprint("[bold green]📚 Books Scraper iniciado[/bold green]")
    if use_ai:
        rprint("[bold magenta]🤖 IA do Groq ativada para parsing de descrições[/bold magenta]")

    # Passamos os novos parâmetros para o pipeline
    result = asyncio.run(pipeline_run(
        max_pages=max_pages, 
        delay=delay, 
        category_url=category_url, 
        use_ai=use_ai,
        search_title=search 
    ))

    rprint("\n[bold]✅ Concluído![/bold]")
    rprint(f"   Livros coletados : [cyan]{result.total_books}[/cyan]")
    rprint(f"   Páginas visitadas: [cyan]{result.total_pages}[/cyan]")
    rprint("   Saída            : [cyan]output/books.json[/cyan] + [cyan]output/books.csv[/cyan]")

if __name__ == "__main__":
    app()