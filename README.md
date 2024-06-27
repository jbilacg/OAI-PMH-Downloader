# **OAI-PMH Downloader**

**Este projeto oferece uma solução para baixar e organizar arquivos e metadados de registros provenientes de um servidor OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting). Utilizando Python, o script faz o download de arquivos (como PDFs e imagens) e extrai informações detalhadas dos metadados em formato XML. Esses dados são então salvos em um arquivo CSV para fácil análise e os arquivos baixados são compactados em um arquivo ZIP.**

## **Recursos**

- **Download de Arquivos**: Baixa arquivos associados aos registros OAI-PMH, como PDFs e imagens.
- **Extração de Metadados**: Extrai e organiza metadados como título, autor, assunto, data, formato, identificador, descrição e relação.
- **Salvamento em CSV**: Salva os metadados extraídos em um arquivo CSV para fácil consulta e análise.
- **Compactação de Arquivos**: Cria um arquivo ZIP contendo todos os arquivos baixados para fácil compartilhamento e armazenamento.

## **Como Funciona**

1. **Download de XML**: O script baixa o conteúdo XML dos registros OAI-PMH de uma URL especificada.
2. **Parsing e Extração**: Faz o parsing do XML e extrai os metadados e links dos arquivos.
3. **Download de Arquivos**: Baixa os arquivos encontrados e os salva em uma pasta especificada.
4. **Salvamento de Metadados**: Salva os metadados em um arquivo CSV.
5. **Criação de ZIP**: Cria um arquivo ZIP contendo todos os arquivos baixados.

**Este projeto é ideal para pesquisadores, bibliotecários e desenvolvedores que precisam coletar, organizar e armazenar grandes quantidades de dados e arquivos de repositórios digitais.**
