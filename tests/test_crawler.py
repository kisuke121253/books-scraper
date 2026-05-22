import pytest
from unittest.mock import patch
from playwright.async_api import async_playwright
from scraper.crawler import extract_book_details, BASE_URL
from scraper.models import Book

BOOK_DETAIL_HTML = """
<!DOCTYPE html>
<html><head><title>A Light In The Attic</title></head>
<body>
    <div class="product_main">
        <h1>A Light in the Attic</h1>
        <p class="price_color">£51.77</p>
        <p class="instock availability"><i class="icon-ok"></i> In stock</p>
        <p class="star-rating Three"></p>
    </div>
    <div id="product_description"></div>
    <p>Descrição teste.</p>
    <table class="table table-striped"><tr><th>UPC</th><td>a897fe</td></tr></table>
</body>
</html>
"""

@pytest.mark.asyncio
async def test_extract_book_details_success():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(BOOK_DETAIL_HTML)
        
        # use_ai=False para não bater no Groq
        details = await extract_book_details(page, "http://test", use_ai=False)
        
        assert details["title"] == "A Light in the Attic"
        assert details["price"] == "51.77"
        assert details["rating"] == 3
        assert details["availability"] is True
        
        await browser.close()

@pytest.mark.asyncio
@patch("scraper.crawler.extract_structured_info_with_groq")
async def test_extract_book_details_with_ai(mock_ai_call):
    # Simulamos o retorno da IA
    mock_ai_call.return_value = {"theme": "Mock IA"}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(BOOK_DETAIL_HTML)
        
        # use_ai=True ativa o fluxo da inteligência artificial
        details = await extract_book_details(page, "http://test", use_ai=True)
        
        assert details["ai_insights"] == {"theme": "Mock IA"}
        mock_ai_call.assert_called_once()
        
        await browser.close()