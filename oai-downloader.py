import requests
import xml.etree.ElementTree as ET
import pandas as pd
import zipfile
import os
import uuid

def download_files_from_xml(xml_content, output_folder):
    """
    Faz o parsing do conteúdo XML e baixa os arquivos encontrados.

    Args:
        xml_content (str): O conteúdo XML contendo os registros.
        output_folder (str): O diretório onde os arquivos baixados serão salvos.

    Returns:
        list: Uma lista de dicionários contendo os metadados dos registros.
    """
    root = ET.fromstring(xml_content)
    namespace = {"oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/"}
    data = []

    for record in root.findall(".//{http://www.openarchives.org/OAI/2.0/}record"):
        metadata = record.find(".//{http://www.openarchives.org/OAI/2.0/oai_dc/}dc")
        row = {}

        # Verificar e extrair os elementos de metadados
        title_elem = metadata.find("{http://purl.org/dc/elements/1.1/}title")
        row['title'] = title_elem.text if title_elem is not None else ''

        creator_elem = metadata.find("{http://purl.org/dc/elements/1.1/}creator")
        row['creator'] = creator_elem.text if creator_elem is not None else ''

        subject_elems = metadata.findall("{http://purl.org/dc/elements/1.1/}subject")
        row['subject'] = [elem.text for elem in subject_elems] if subject_elems else []

        date_elem = metadata.find("{http://purl.org/dc/elements/1.1/}date")
        row['date'] = date_elem.text if date_elem is not None else ''

        format_elems = metadata.findall("{http://purl.org/dc/elements/1.1/}format")
        row['format'] = [elem.text for elem in format_elems] if format_elems else []

        identifier_elems = metadata.findall("{http://purl.org/dc/elements/1.1/}identifier")
        row['identifier'] = [elem.text for elem in identifier_elems] if identifier_elems else []

        description_elems = metadata.findall("{http://purl.org/dc/elements/1.1/}description")
        row['description'] = [elem.text for elem in description_elems] if description_elems else []

        relation_elems = metadata.findall("{http://purl.org/dc/elements/1.1/}relation")
        row['relation'] = [elem.text for elem in relation_elems] if relation_elems else []

        data.append(row)

        # Baixar arquivos associados ao registro
        for link in record.findall(".//{http://www.w3.org/2005/Atom}link"):
            link_href = link.get("href")
            if link_href.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                file_name = os.path.basename(link_href)
                file_name, file_extension = os.path.splitext(file_name)
                unique_suffix = str(uuid.uuid4())[:8]
                unique_file_name = f"{file_name}_{unique_suffix}{file_extension}"
                download_file(link_href, os.path.join(output_folder, unique_file_name))
                row['file_name'] = unique_file_name

    if not data:
        print("Nenhum arquivo para baixar encontrado.")

    return data

def download_file(url, filename):
    """
    Faz o download de um arquivo de uma URL e salva no diretório especificado.

    Args:
        url (str): A URL do arquivo a ser baixado.
        filename (str): O caminho completo onde o arquivo será salvo.
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Arquivo '{filename}' baixado com sucesso!")
    else:
        print(f"Erro ao baixar o arquivo '{filename}'.")

def save_to_csv(data, csv_filename):
    """
    Salva os dados em um arquivo CSV.

    Args:
        data (list): Os dados a serem salvos.
        csv_filename (str): O nome do arquivo CSV.
    """
    df = pd.DataFrame(data)
    df.to_csv(csv_filename, index=False)
    print("Dados salvos em", csv_filename)

# URL base do OAI-PMH
base_url = 'http://atom.ape.es.gov.br/;oai?verb=ListRecords&set=_15249&metadataPrefix=oai_dc'

# Pasta para salvar os arquivos baixados
output_folder = 'Professora Alpia Couto'

# Nome do arquivo CSV
csv_filename = 'Professora Alpia Couto.csv'

# Nome do arquivo ZIP
zip_filename = 'Professora Alpia Couto.zip'

# Defina o token de resumption inicial como vazio
resumption_token = None

# Inicialize a lista de dados para armazenar todos os registros
all_data = []

while True:
    # Construa a URL da página atual
    url = f'{base_url}&resumptionToken={resumption_token}' if resumption_token else base_url

    # Faça o download do XML OAI-PMH
    xml_content = requests.get(url).content

    # Faça o parsing do XML e obtenha os dados
    data = download_files_from_xml(xml_content, output_folder)

    # Agregue os dados à lista geral
    all_data.extend(data)

    # Obtenha o novo token de resumption, se houver
    root = ET.fromstring(xml_content)
    new_resumption_token = root.find(".//{http://www.openarchives.org/OAI/2.0/}resumptionToken")
    if new_resumption_token is not None:
        resumption_token = new_resumption_token.text
    else:
        break  # Saia do loop se não houver mais páginas

# Adicione sufixos únicos aos nomes dos arquivos no DataFrame
for row in all_data:
    if 'file_name' in row:
        file_name, file_extension = os.path.splitext(row['file_name'])
        unique_suffix = str(uuid.uuid4())[:8]
        unique_file_name = f"{file_name}_{unique_suffix}{file_extension}"
        row['file_name'] = unique_file_name

# Salve os dados em um arquivo CSV
save_to_csv(all_data, csv_filename)

# Crie um arquivo ZIP com os arquivos baixados
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, output_folder))

print("Arquivo ZIP criado:", zip_filename)
