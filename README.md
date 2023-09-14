# Projeto de Verificação de Dados em Arquivos ZIP (ex. PTUA500)

Este projeto é um script Python desenvolvido para verificar dados em arquivos ZIP que contêm XML e PDF. O objetivo é extrair informações de arquivos XML dentro de arquivos ZIP e compará-las com os dados extraídos de arquivos PDF para garantir sua integridade e consistência.

## Pré-requisitos

Antes de executar o script, você deve garantir que seu ambiente Python atenda aos seguintes requisitos:

- Python 3.x instalado
- Bibliotecas necessárias instaladas (você pode instalá-las usando `pip install`):
  - tkinter
  - xml.etree.ElementTree
  - pdfplumber
  - locale
  - zipfile

## Como Usar

1. Execute o script Python fornecido.
2. Uma janela de seleção de diretório será exibida. Selecione o diretório raiz que contém os arquivos ZIP a serem processados.
3. O script irá:
   - Extrair os arquivos XML e PDF de cada arquivo ZIP encontrado no diretório.
   - Comparar os dados extraídos dos arquivos XML com os dados extraídos dos arquivos PDF.
   - Imprimir qualquer inconsistência encontrada, como diferenças na data de emissão ou no valor total.

## Palavras-chave

Se você está buscando por ferramentas relacionadas a:

- Verificação de dados em documentos eletrônicos
- Comparação de informações entre arquivos XML e PDF
- Processamento de arquivos ZIP com dados XML e PDF
- Validação de documentos financeiros ou regulatórios
- Verificação de integridade de documentos
- PTU A500
- Unimed
- Intercâmbio Unimed

Este projeto pode ser útil para você!

