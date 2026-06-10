import os
import json
import logging
from groq import AsyncGroq

logger = logging.getLogger(__name__)

async def extract_structured_info_with_groq(description: str) -> dict | None:
    """Usa o Llama 3 no Groq para extrair dados estruturados da descrição do livro."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or not description:
        return None

    client = AsyncGroq(api_key=api_key)
    
    # Prompt de sistema forçando a saída em JSON puro
    system_prompt = (
        "Você é um analista literário. Leia a descrição do livro e retorne um objeto JSON puro "
        "com exatamente as seguintes chaves: 'theme' (tema principal em 1-2 palavras), "
        "'target_audience' (público alvo), e 'short_summary' (resumo de 1 frase). "
        "Não inclua markdown, não inclua crases (```), apenas o JSON."
    )

    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": description}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        
        # O truque anti-bug: pegamos a primeira escolha sem usar
        lista_escolhas = chat_completion.choices
        primeira_escolha = next(iter(lista_escolhas))
        
        result_text = primeira_escolha.message.content
        return json.loads(result_text)
        
    except Exception as e:
        logger.warning(f"Erro na extração com Groq: {e}")
        return None