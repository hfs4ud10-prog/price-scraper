"""
main.py

Ponto de entrada do projeto. Define as páginas a serem coletadas,
executa o scraping, gera os arquivos de saída e exibe o resumo final.
"""

from scraper import scrape_pages
from exporter import (
    criar_dataframe,
    filtrar_por_preco,
    exportar_csv,
    exportar_excel,
    exibir_confirmacao_exportacao,
    exibir_resumo,
)

URL_BASE = "https://books.toscrape.com/"

# Lista de páginas que serão coletadas. O site possui paginação no formato
# .../catalogue/page-2.html, .../catalogue/page-3.html, etc.
PAGINAS_PARA_COLETAR = [
    URL_BASE,
    URL_BASE + "catalogue/page-2.html",
    URL_BASE + "catalogue/page-3.html",
]

# Preço máximo (em libras) usado no filtro opcional.
PRECO_MAXIMO_FILTRO = 30


def main():
    """Executa o fluxo completo: coleta, filtro, exportação e resumo."""
    print(f"Iniciando coleta em {len(PAGINAS_PARA_COLETAR)} página(s)...\n")

    livros = scrape_pages(PAGINAS_PARA_COLETAR)

    if not livros:
        print("Nenhum livro foi coletado. Encerrando.")
        return

    df_livros = criar_dataframe(livros)

    # O filtro por preço é aplicado antes da exportação: os arquivos CSV/Excel
    # gerados refletem apenas os livros dentro do limite definido acima.
    df_filtrado = filtrar_por_preco(df_livros, preco_maximo=PRECO_MAXIMO_FILTRO)

    exportar_csv(df_filtrado)
    exportar_excel(df_filtrado)
    exibir_confirmacao_exportacao(df_filtrado)

    exibir_resumo(df_livros, df_filtrado)


if __name__ == "__main__":
    main()