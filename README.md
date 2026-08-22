# Price Scraper — Books to Scrape

Web scraper desenvolvido em Python para coletar informações de livros do site [Books to Scrape](https://books.toscrape.com/) e exportar os dados para arquivos **CSV** e **Excel**.

O projeto coleta título, preço, disponibilidade, avaliação e URL dos livros, possui filtro opcional por preço máximo e apresenta um resumo estatístico da coleta no terminal.

Projeto desenvolvido para praticar **web scraping, manipulação de dados, exportação de arquivos, tratamento de erros e organização de um projeto Python**.

---

## 🚀 Funcionalidades

- Coleta de informações de livros utilizando HTTP requests.
- Extração de dados HTML com BeautifulSoup.
- Coleta de múltiplas páginas.
- Filtro opcional por preço máximo.
- Exportação dos resultados para CSV.
- Exportação dos resultados para Excel.
- Formatação automática da planilha Excel.
- URLs dos livros como hyperlinks clicáveis.
- Filtros e ordenação diretamente no Excel.
- Resumo estatístico da coleta no terminal.
- Tratamento de erros de conexão, timeout e HTTP.
- Continuidade da coleta mesmo quando uma página apresenta erro.

---

## 🛠️ Tecnologias utilizadas

| Biblioteca | Função no projeto |
|---|---|
| [`requests`](https://docs.python-requests.org/) | Realiza as requisições HTTP para baixar o HTML das páginas. |
| [`beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/) | Analisa o HTML e localiza as informações de cada livro. |
| [`pandas`](https://pandas.pydata.org/) | Organiza os dados em DataFrames, permitindo filtros, manipulação e cálculos estatísticos. |
| [`openpyxl`](https://openpyxl.readthedocs.io/) | Utilizada pelo pandas para gerar e formatar arquivos `.xlsx`. |

---

## 📁 Estrutura do projeto

```text
price_scraper/
│
├── src/
│   ├── scraper.py      # Coleta e extração dos dados
│   ├── exporter.py     # Tratamento e exportação dos dados
│   └── main.py         # Execução e orquestração do projeto
│
├── output/
│   └── .gitkeep        # Mantém a pasta no Git
│
├── requirements.txt    # Dependências do projeto
├── README.md           # Documentação
└── .gitignore          # Arquivos ignorados pelo Git

Os arquivos livros.csv e livros.xlsx são gerados automaticamente durante a execução e não são necessários no repositório.

⚙️ Instalação
1. Clone o repositório
git clone https://github.com/seu-usuario/price_scraper.git
cd price_scraper
2. Crie um ambiente virtual
python -m venv .venv
3. Ative o ambiente virtual

Windows:

.venv\Scripts\activate

Linux/Mac:

source .venv/bin/activate
4. Instale as dependências
pip install -r requirements.txt
▶️ Execução

Com o ambiente virtual ativado:

python src/main.py

O programa irá:

Coletar os livros das páginas configuradas em PAGINAS_PARA_COLETAR.
Processar os dados encontrados.
Aplicar o filtro de preço, caso configurado.
Gerar output/livros.csv.
Gerar output/livros.xlsx.
Exibir um resumo da coleta no terminal.
Coletando mais páginas

As URLs utilizadas na coleta podem ser configuradas em main.py através da lista PAGINAS_PARA_COLETAR.

Por exemplo:

PAGINAS_PARA_COLETAR = [
    "https://books.toscrape.com/",
    "https://books.toscrape.com/catalogue/page-2.html",
    "https://books.toscrape.com/catalogue/page-3.html",
    "https://books.toscrape.com/catalogue/page-4.html",
]
🔄 Funcionamento

O fluxo geral do projeto segue estas etapas:

URLs
 ↓
Requests
 ↓
Download do HTML
 ↓
BeautifulSoup
 ↓
Extração dos dados
 ↓
DataFrame (Pandas)
 ↓
Filtro por preço (opcional)
 ↓
CSV + Excel
 ↓
Resumo estatístico
Coleta

A função principal de coleta é scrape_pages(urls), localizada em scraper.py.

from scraper import scrape_pages

urls = [
    "https://books.toscrape.com/",
    "https://books.toscrape.com/catalogue/page-2.html",
]

livros = scrape_pages(urls)

A função recebe uma lista de URLs, coleta os livros encontrados em cada página e retorna uma lista única com os resultados.

Caso uma página apresente um erro de conexão, timeout, erro HTTP ou não contenha livros, ela é ignorada e a coleta continua nas demais páginas.

💰 Filtro por preço

O projeto possui um filtro opcional para limitar os resultados de acordo com o preço máximo.

Por exemplo:

from exporter import criar_dataframe, filtrar_por_preco

df = criar_dataframe(livros)

df_baratos = filtrar_por_preco(
    df,
    preco_maximo=30
)

Nesse exemplo, preco_maximo=30 mantém somente livros com preço igual ou inferior a £30.

O filtro é aplicado antes da exportação, permitindo gerar arquivos contendo apenas os produtos dentro da faixa de preço desejada.

📊 Resultados
Excel

O arquivo livros.xlsx recebe formatação para facilitar a leitura e análise dos dados:

Cabeçalho em negrito e centralizado.
Larguras das colunas ajustadas ao conteúdo.
Coluna preco mantida como número.
Preços exibidos no formato £51.77.
Coluna rating mantida como número inteiro.
URLs convertidas em hyperlinks clicáveis.
Primeira linha congelada com freeze_panes.
Dados convertidos em uma Tabela do Excel.
Autofiltro disponível diretamente nos cabeçalhos.
Estilo de linhas alternadas para facilitar a leitura.
Possibilidade de ordenar e filtrar qualquer coluna diretamente no Excel.

Nenhum dado é alterado durante a formatação; as alterações são exclusivamente visuais e estruturais para melhorar a apresentação da planilha.

CSV

O arquivo livros.csv utiliza uma configuração compatível com o Excel em português/Brasil:

df.to_csv(
    caminho,
    index=False,
    encoding="utf-8-sig",
    sep=";",
    decimal=","
)
sep=";" — utiliza ponto e vírgula como separador de colunas.
decimal="," — utiliza vírgula como separador decimal.
encoding="utf-8-sig" — preserva corretamente acentos e caracteres especiais no Excel do Windows.
index=False — evita a criação de uma coluna adicional contendo o índice do DataFrame.

Essa configuração facilita a abertura do CSV diretamente no Excel configurado para português/Brasil.

🖥️ Exemplo de saída
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

Os valores acima são ilustrativos. A quantidade e os preços dos livros dependem das páginas coletadas durante a execução.

🛡️ Tratamento de erros

O projeto trata diferentes situações que podem ocorrer durante a coleta:

Erro de conexão
requests.exceptions.ConnectionError

Ocorre, por exemplo, quando não é possível estabelecer conexão com o servidor.

Timeout

As requisições possuem limite de 10 segundos, evitando que uma página indisponível interrompa indefinidamente o programa.

Erros HTTP

Erros como 404 Not Found e outros códigos HTTP são identificados através de:

resposta.raise_for_status()
HTML inesperado

Caso nenhuma informação de livro seja encontrada na página, um aviso é exibido e a página é ignorada.

Campos ausentes

Livros sem informações essenciais, como título ou preço, são descartados individualmente sem interromper o restante da coleta.

Cada página possui seu próprio tratamento de exceções, permitindo que um erro em uma URL não interrompa a coleta das demais.

📸 Demonstração
Terminal

Excel

As imagens acima demonstram a execução do scraper e a formatação dos dados exportados.

🔮 Melhorias futuras
 Detectar automaticamente o número total de páginas.
 Coletar todas as páginas automaticamente.
 Armazenar os dados em SQLite ou PostgreSQL.
 Criar histórico de preços.
 Gerar gráficos de variação de preços.
 Agendar execuções periódicas com cron ou APScheduler.
 Adicionar testes automatizados com pytest.
 Utilizar mocks para testar respostas HTTP.
 Implementar logging estruturado utilizando o módulo logging.
📚 Sobre o projeto

Este projeto utiliza o Books to Scrape, um site criado especificamente para praticar web scraping.

O objetivo do projeto é demonstrar conhecimentos práticos de:

Python
Web scraping
HTTP requests
Parsing de HTML
Pandas
Manipulação de dados
Exportação CSV/Excel
Tratamento de exceções
Organização de código
Documentação de projetos
