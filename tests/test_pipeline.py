import pytest
from unittest.mock import patch
from scraper.pipeline import run

@pytest.mark.asyncio
@patch("scraper.pipeline.run_playwright_scraper")
@patch("scraper.pipeline.save_results")
async def test_pipeline_run_success(mock_save, mock_crawler):
    # Simulamos o crawler devolvendo 1 livro válido
    mock_crawler.return_value = ([{
        "title": "Mock Book",
        "price": "10.00",
        "rating": 5,
        "availability": True,
        "url": "http://mock",
        "upc": "123",
        "description": "Mock desc",
        "ai_insights": None
    }], 1)

    # Passamos os novos parâmetros do Modo Caçador e Categorias
    result = await run(max_pages=1, use_ai=False, search_title="Mock", category_url=None)

    assert result.total_books == 1
    assert result.total_pages == 1
    
    # Truque anti-bug de colchetes:
    primeiro_livro = next(iter(result.books))
    assert primeiro_livro.title == "Mock Book"
    
    mock_save.assert_called_once()

@pytest.mark.asyncio
@patch("scraper.pipeline.run_playwright_scraper")
@patch("scraper.pipeline.save_results")
async def test_pipeline_ignores_invalid_books(mock_save, mock_crawler):
    # Simulamos um dicionário faltando o preço (deve ser barrado pelo Pydantic)
    invalid_book = {"title": "No Price Book", "rating": 5, "availability": True, "url": "http://x"}
    mock_crawler.return_value = ([invalid_book], 1)

    result = await run()

    # O pipeline deve engolir o erro e retornar 0 livros processados
    assert result.total_books == 0