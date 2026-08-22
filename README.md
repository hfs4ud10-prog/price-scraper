# Price Scraper — Books to Scrape

## Descrição

Web scraper em Python que acessa o site estático [books.toscrape.com](https://books.toscrape.com/), extrai informações de livros (título, preço, disponibilidade, avaliação e URL) e exporta os resultados para arquivos **CSV** e **Excel**. O projeto também oferece um filtro opcional por preço máximo e exibe um resumo estatístico da coleta no terminal.

Este projeto foi desenvolvido como solução para o desafio técnico "Scraper de Preços Simples", de nível Entry.

## Tecnologias utilizadas

| Biblioteca | Função no projeto |
|---|---|
| [`requests`](https://docs.python-requests.org/) | Realiza as requisições HTTP para baixar o HTML das páginas. |
| [`beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/) | Analisa (parseia) o HTML e localiza as informações de cada livro. |
| [`pandas`](https://pandas.pydata.org/) | Organiza os dados coletados em uma estrutura tabular (DataFrame), permitindo filtros e cálculos estatísticos. |
| [`openpyxl`](https://openpyxl.readthedocs.io/) | Usada pelo pandas como "motor" para gerar arquivos `.xlsx` (Excel). |

## Estrutura do projeto

```text
price_scraper/
│
├── src/
│   ├── scraper.py      # Requisições HTTP e extração de dados (HTML -> dicionários)
│   ├── exporter.py      # DataFrame, filtro, exportação CSV/Excel e resumo
│   └── main.py           # Orquestra o fluxo completo do programa
│
├── output/
│   ├── livros.csv        # Gerado automaticamente ao executar o projeto
│   └── livros.xlsx       # Gerado automaticamente ao executar o projeto
│
├── requirements.txt
├── README.md
└── .gitignore
```

> **Por que essa estrutura?** Para um projeto Entry, uma divisão em três módulos (`scraper`, `exporter`, `main`) já é suficiente para separar responsabilidades (coleta, tratamento/exportação e orquestração) sem introduzir complexidade desnecessária, como pacotes aninhados, camadas de configuração ou testes automatizados. Isso mantém o código fácil de ler e de apresentar em portfólio, sem parecer um projeto "inchado" para o nível proposto.

## Instalação

1. Clone ou baixe este projeto:

```bash
git clone https://github.com/hfs4ud10-prog/price_scraper.git
cd price_scraper
```

2. Crie um ambiente virtual:

```bash
python -m venv .venv
```

3. Ative o ambiente virtual:

```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

Com o ambiente virtual ativado, execute:

```bash
cd src
python main.py
```

O programa irá:

1. Coletar os livros das páginas configuradas em `PAGINAS_PARA_COLETAR` (dentro de `main.py`).
2. Gerar os arquivos `output/livros.csv` e `output/livros.xlsx`.
3. Exibir um resumo da coleta no terminal.

Para coletar mais páginas, basta adicionar novas URLs à lista `PAGINAS_PARA_COLETAR` em `main.py`, por exemplo `.../catalogue/page-4.html`.

## Funcionamento

O fluxo geral do projeto segue estas etapas:

```text
URLs
 ↓
requests           (baixa o HTML de cada página)
 ↓
BeautifulSoup       (analisa o HTML)
 ↓
extração dos dados  (título, preço, disponibilidade, rating, URL)
 ↓
DataFrame           (pandas organiza os dados em tabela)
 ↓
filtro              (opcional: filtro por preço máximo)
 ↓
CSV + Excel         (arquivos exportados para output/)
 ↓
resumo              (estatísticas exibidas no terminal)
```

A função central de coleta é `scrape_pages(urls)`, em `scraper.py`:

```python
from scraper import scrape_pages

urls = [
    "https://books.toscrape.com/",
    "https://books.toscrape.com/catalogue/page-2.html",
]

livros = scrape_pages(urls)
```

Ela recebe uma lista de URLs, coleta os livros de cada uma e retorna uma lista única com todos os resultados, ignorando páginas que falharem.

O filtro por preço é usado assim (`exporter.py`):

```python
from exporter import criar_dataframe, filtrar_por_preco

df = criar_dataframe(livros)
df_baratos = filtrar_por_preco(df, preco_maximo=30)
```

## Exemplo de saída

```text
Iniciando coleta em 3 página(s)...

Coletando: https://books.toscrape.com/
  -> 20 livro(s) encontrado(s)
Coletando: https://books.toscrape.com/catalogue/page-2.html
  -> 20 livro(s) encontrado(s)
Coletando: https://books.toscrape.com/catalogue/page-3.html
  -> 20 livro(s) encontrado(s)
Arquivo CSV salvo em: output/livros.csv
Arquivo Excel salvo em: output/livros.xlsx

===== EXPORTAÇÃO CONCLUÍDA =====

CSV:
  output/livros.csv

Excel:
  output/livros.xlsx

Prévia dos dados (5 primeiras linhas):
               titulo  preco disponibilidade  rating                                                      url
A Light in the Attic   51.77       In stock        3   https://books.toscrape.com/catalogue/a-light-in-...
  Tipping the Velvet   53.74       In stock        1   https://books.toscrape.com/catalogue/tipping-the...
...

=================================

===== RESUMO =====
Livros coletados: 60
Livros após filtro: 27
Preço médio: £35.42
Livro mais barato: In Her Wake (£12.84)
Livro mais caro: The Requiem Red (£58.63)
Distribuição das avaliações:
  1 estrela(s): 12 livro(s)
  2 estrela(s): 11 livro(s)
  3 estrela(s): 15 livro(s)
  4 estrela(s): 11 livro(s)
  5 estrela(s): 11 livro(s)
===================
```

*(Os valores acima são ilustrativos; a saída real depende dos livros presentes nas páginas coletadas no momento da execução.)*

## Formatação dos arquivos de saída

### `livros.xlsx`

A planilha é gerada com `pandas` + `openpyxl` e recebe formatação profissional:

* cabeçalho em **negrito** e centralizado;
* larguras de coluna ajustadas ao conteúdo (título e URL mais largos; preço e avaliação mais estreitos);
* coluna `preco` mantida como número, exibida no formato `£51.77`;
* coluna `rating` mantida como número inteiro;
* URLs como **hyperlinks clicáveis**;
* primeira linha **congelada** (`freeze_panes`), permanecendo visível ao rolar;
* dados convertidos em uma **Tabela do Excel** (`TabelaLivros`), com autofiltro e estilo de faixas alternadas — permitindo ordenar e filtrar qualquer coluna direto pelo cabeçalho.

Nenhum dado é alterado nesse processo — apenas a apresentação visual da planilha.

### `livros.csv`

O CSV é gerado com uma configuração pensada para abrir corretamente no Excel em português/Brasil:

```python
df.to_csv(caminho, index=False, encoding="utf-8-sig", sep=";", decimal=",")
```

* **`sep=";"`**: o Excel em configuração pt-BR usa `,` como separador decimal; se o CSV também usasse `,` para separar colunas, o Excel confundiria os dois e jogaria tudo em uma única coluna. Usar `;` evita esse conflito.
* **`decimal=","`**: mantém a convenção numérica brasileira (`51,77` em vez de `51.77`), para que o Excel reconheça a coluna `preco` como número, não como texto.
* **`encoding="utf-8-sig"`**: adiciona um BOM no início do arquivo, garantindo que acentos e caracteres especiais sejam exibidos corretamente ao abrir no Excel do Windows.
* **`index=False`**: evita uma coluna extra com o índice do DataFrame.

## Tratamento de erros

O projeto trata especificamente os seguintes cenários, sem interromper a coleta das demais páginas:

* **Erro de conexão** (`requests.exceptions.ConnectionError`) — ex.: sem internet, domínio inexistente.
* **Timeout** (`requests.exceptions.Timeout`) — a requisição é limitada a 10 segundos.
* **Erros HTTP** (`requests.exceptions.HTTPError`), incluindo `404 Not Found` e outros status de erro, verificados via `resposta.raise_for_status()`.
* **HTML inesperado** — se nenhum livro for encontrado na página, um aviso é exibido e a página é simplesmente ignorada.
* **Campos ausentes** — livros sem título ou preço são descartados individualmente, sem interromper o processamento dos demais.

Em todos os casos, o erro é registrado no terminal e o programa segue para a próxima página, graças à função `scrape_pages`, que envolve cada requisição em seu próprio tratamento de exceções.

## Melhorias futuras

* Detectar automaticamente o número total de páginas e coletar todas sem precisar listá-las manualmente.
* Armazenar os dados em um banco de dados (ex.: SQLite ou PostgreSQL) em vez de apenas CSV/Excel.
* Agendar execuções periódicas (ex.: com `cron` ou `APScheduler`) para acompanhar variações de preço.
* Guardar um histórico de preços e gerar gráficos de variação ao longo do tempo.
* Adicionar testes automatizados (ex.: com `pytest`), incluindo mocks das respostas HTTP.
* Adicionar logging estruturado (módulo `logging`) no lugar dos `print()` atuais.
