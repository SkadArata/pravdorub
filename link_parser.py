# link_parser.py
import requests
from bs4 import BeautifulSoup
import trafilatura

async def extract_article(url: str) -> str:
    """Извлекает текст статьи из URL"""
    try:
        if not url.startswith(('http://', 'https://')):
            return f"❌ Неверная ссылка: {url}"

        print(f"🌐 Парсим: {url}")

        # Trafilatura — основной вариант для новостей
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded)
            if text:
                # Ограничим, скажем, 3000 символами для модели
                return text[:3000]

        # Fallback: BeautifulSoup
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1') or soup.find('title')
        title_text = title.get_text().strip() if title else "Без заголовка"

        paragraphs = soup.find_all('p')[:5]
        content = ' '.join([p.get_text().strip() for p in paragraphs])[:3000]

        return f"{title_text}\n\n{content}" if content else title_text

    except Exception as e:
        return f"❌ Ошибка парсинга: {str(e)}"
