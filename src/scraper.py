"""
scraper.py

Responsável por acessar as páginas do site https://books.toscrape.com/,
extrair os dados dos livros e tratar os erros de rede/HTTP que possam ocorrer.
"""

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Headers "educados" para identificar o scraper e evitar bloqueios simples.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; PriceScraperBot/1.0; "
        "+https://github.com/seu-usuario/price_scraper)"
    )
}

# Tempo máximo (em segundos) de espera por uma resposta do servidor.
TIMEOUT_SEGUNDOS = 10

# Mapeamento das classes CSS de rating (texto -> número) usadas pelo site.
RATINGS_TEXTO_PARA_NUMERO = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def buscar_html(url):
    """
    Faz uma requisição HTTP GET para a URL informada e retorna o HTML da página.

    Trata especificamente erros de conexão, timeout e status HTTP de erro,
    retornando None quando a página não pode ser obtida (em vez de interromper
    a execução do programa).
    """
    try:
        resposta = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SEGUNDOS)
        resposta.raise_for_status()
    except requests.exceptions.Timeout:
        print(f"[ERRO] Tempo de espera esgotado ao acessar: {url}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"[ERRO] Falha de conexão ao acessar: {url}")
        return None
    except requests.exceptions.HTTPError as erro:
        print(f"[ERRO] Erro HTTP ({erro.response.status_code}) ao acessar: {url}")
        return None
    except requests.exceptions.RequestException as erro:
        # Rede de segurança para outros erros da biblioteca requests
        # (ex.: URL malformada), sem mascarar erros de programação.
        print(f"[ERRO] Erro inesperado de requisição ao acessar {url}: {erro}")
        return None

    return resposta.text


def _extrair_preco(livro_tag):
    """Extrai e limpa o preço de um livro a partir da sua tag HTML."""
    tag_preco = livro_tag.find("p", class_="price_color")
    if tag_preco is None:
        return None

    # O site retorna algo como "£51.77"; removemos o símbolo da moeda.
    texto_preco = tag_preco.get_text(strip=True)
    return texto_preco.replace("£", "").replace("Â", "").strip()


def _extrair_disponibilidade(livro_tag):
    """Extrai o texto de disponibilidade (ex.: 'In stock')."""
    tag_disponibilidade = livro_tag.find("p", class_="instock availability")
    if tag_disponibilidade is None:
        return "Indisponível"
    return tag_disponibilidade.get_text(strip=True)


def _extrair_rating(livro_tag):
    """Converte a classe CSS de rating (ex.: 'star-rating Three') em número."""
    tag_rating = livro_tag.find("p", class_="star-rating")
    if tag_rating is None:
        return None

    classes = tag_rating.get("class", [])
    for classe in classes:
        if classe in RATINGS_TEXTO_PARA_NUMERO:
            return RATINGS_TEXTO_PARA_NUMERO[classe]
    return None


def _extrair_titulo_e_url(livro_tag, url_base):
    """Extrai o título completo e a URL absoluta do livro."""
    tag_link = livro_tag.h3.find("a") if livro_tag.h3 else None
    if tag_link is None:
        return None, None

    # O atributo "title" contém o título completo, sem truncar.
    titulo = tag_link.get("title", "").strip()
    url_relativa = tag_link.get("href", "")
    url_completa = urljoin(url_base, url_relativa)
    return titulo, url_completa


def extrair_livros_da_pagina(html, url_base):
    """
    Recebe o HTML de uma página de listagem e retorna uma lista de dicionários,
    um para cada livro encontrado.

    Livros com campos essenciais ausentes (título ou preço) são ignorados,
    mas não interrompem o processamento dos demais.
    """
    livros_encontrados = []
    soup = BeautifulSoup(html, "html.parser")

    tags_de_livros = soup.find_all("article", class_="product_pod")
    if not tags_de_livros:
        print("[AVISO] Nenhum livro encontrado nesta página (HTML inesperado?).")
        return livros_encontrados

    for livro_tag in tags_de_livros:
        titulo, url_livro = _extrair_titulo_e_url(livro_tag, url_base)
        preco = _extrair_preco(livro_tag)

        if titulo is None or preco is None:
            print("[AVISO] Livro ignorado por falta de título ou preço.")
            continue

        livro = {
            "titulo": titulo,
            "preco": preco,
            "disponibilidade": _extrair_disponibilidade(livro_tag),
            "rating": _extrair_rating(livro_tag),
            "url": url_livro,
        }
        livros_encontrados.append(livro)

    return livros_encontrados


def scrape_pages(urls):
    """
    Recebe uma lista de URLs de páginas de listagem do books.toscrape.com
    e retorna uma lista consolidada de dicionários com os dados dos livros.

    Uma página com erro (de conexão, HTTP ou HTML inesperado) não impede
    que as demais páginas da lista sejam processadas.
    """
    todos_os_livros = []

    for url in urls:
        print(f"Coletando: {url}")
        html = buscar_html(url)

        if html is None:
            # Erro já foi reportado em buscar_html(); seguimos para a próxima página.
            continue

        livros_da_pagina = extrair_livros_da_pagina(html, url)
        print(f"  -> {len(livros_da_pagina)} livro(s) encontrado(s)")
        todos_os_livros.extend(livros_da_pagina)

    return todos_os_livros
