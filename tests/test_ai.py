import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from scraper.ai_enrichment import extract_structured_info_with_groq

@pytest.mark.asyncio
@patch("scraper.ai_enrichment.AsyncGroq")
async def test_extract_structured_info_success(mock_groq_class):
    # 1. Cria a estrutura de dados exata que o Groq devolve
    mock_message = MagicMock()
    mock_message.content = '{"theme": "Tech", "target_audience": "Devs", "short_summary": "Code."}'
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    
    # Montamos a resposta mockada
    mock_response = MagicMock()
    # Usamos append para não usar colchetes na criação da lista
    lista_falsa = []
    lista_falsa.append(mock_choice)
    mock_response.choices = lista_falsa
    
    # 2. Configura a função create() para ser assíncrona e devolver a resposta
    mock_client = mock_groq_class.return_value
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    # 3. Roda o teste com a variável de ambiente forçada via patch.dict
    with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
        result = await extract_structured_info_with_groq("Livro sobre Python.")
        assert result is not None
        assert result["theme"] == "Tech"

@pytest.mark.asyncio
async def test_extract_structured_info_no_key():
    # Testa o retorno None caso falte a API Key
    with patch.dict(os.environ, {}, clear=True):
        result = await extract_structured_info_with_groq("Desc")
        assert result is None