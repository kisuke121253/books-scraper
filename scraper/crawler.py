import asyncio
import logging
from playwright.async_api import async_playwright, Page
from scraper.models import RATING_MAP
from scraper.ai_enrichment import extract_structured_info_with_groq # Importamos o Groq

logger = logging.getLogger(__name__)

BASE_URL = "https://books.toscrape.com"

async def extract_book_details(page: Page, url: str, use_ai: bool = False) -> dict:
    """Abre a página do livro e extrai os detalhes completos."""
    
    if page.url != url and not url.startswith("http://test"):
        await page.goto(url)
    
    title = await page.locator("h1").first.inner_text()
    price_text = await page.locator("p.price_color").first.inner_text()
    price = price_text.replace("£", "").strip()
    
    stock_text = await page.locator("p.instock.availability").first.inner_text()
    availability = "in stock" in stock_text.lower()
    
    rating_class = await page.locator("p.star-rating").first.get_attribute("class")
    rating_word = rating_class.split()[-1] if rating_class else "One"
    rating = RATING_MAP.get(rating_word, 1)
    
    upc = await page.locator("table tr:nth-child(1) td").first.inner_text()
    
    desc_locator = page.locator("#product_description ~ p")
    description = await desc_locator.first.inner_text() if await desc_locator.count() > 0 else ""

    # SE A IA ESTIVER ATIVADA, ENRIQUECE OS DADOS AQUI
    ai_insights = None
    if use_ai and description:
        ai_insights = await extract_structured_info_with_groq(description)

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
        "url": url,
        "upc": upc,
        "description": description,
        "ai_insights": ai_insights
    }

async def run_playwright_scraper(
    max_pages: int | None = None, 
    delay: float = 0.5, 
    category_url: str | None = None,
    use_ai: bool = False,
    search_title: str | None = None # NOVO PARÂMETRO
) -> tuple[list[dict], int]:
    
    books_data = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="books-scraper/1.0")
        page = await context.new_page()
        
        current_page_url = category_url if category_url else f"{BASE_URL}/catalogue/page-1.html"
        pages_visited = 0
        book_urls = []
        found_target = False # Flag para saber se achamos o alvo

        while current_page_url and not found_target:
            pages_visited += 1
            await page.goto(current_page_url)
            await asyncio.sleep(delay)
            
            links = await page.locator("h3 a").all()
            for link in links:
                # O título completo do livro fica escondido no atributo 'title' do link
                title_attr = await link.get_attribute("title")
                
                # Se estamos buscando e o título não bate, ignoramos e vamos pro próximo
                if search_title and search_title.lower() not in title_attr.lower():
                    continue

                href = await link.get_attribute("href")
                if href:
                    clean_href = href.replace("../", "").replace("./", "")
                    book_urls.append(f"{BASE_URL}/catalogue/{clean_href}")
                
                # Se achamos o que queríamos, avisamos o robô para parar de caçar
                if search_title:
                    found_target = True
                    break 
            
            # Se achou o livro, quebra o while de paginação
            if found_target or (max_pages and pages_visited >= max_pages):
                break
                
            next_btn = page.locator("li.next > a")
            if await next_btn.count() > 0:
                next_url = await next_btn.first.get_attribute("href")
                if "category" in current_page_url:
                    base_path = current_page_url.rsplit("/", 1)
                    current_page_url = f"{base_path}/{next_url}"
                else:
                    current_page_url = f"{BASE_URL}/catalogue/{next_url}"
            else:
                current_page_url = None

        # Agora ele processa apenas a URL do livro que ele encontrou
        for url in book_urls:
            try:
                book_detail = await extract_book_details(page, url, use_ai)
                books_data.append(book_detail)
                await asyncio.sleep(delay)
            except Exception as e:
                logger.warning(f"Falha ao extrair {url}: {e}")

        await browser.close()
        
    return books_data, pages_visited