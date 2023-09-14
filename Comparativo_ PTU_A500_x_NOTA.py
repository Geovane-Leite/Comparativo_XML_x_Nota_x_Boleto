import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
import xml.etree.ElementTree as ET
import pdfplumber
from datetime import datetime
import locale
import zipfile

# Configurar o local para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

# Namespace do XML
namespace = {'ptuA500': 'http://ptu.unimed.coop.br/schemas/V2_1'}

# Função para extrair informações do arquivo XML sem considerar o namespace
def extrair_info_xml(arquivo_xml):
    tree = ET.parse(arquivo_xml)
    root = tree.getroot()
    
    nr_Documento = root.find('.//ptuA500:nr_Documento', namespace)
    dt_EmissaoDoc = root.find('.//ptuA500:dt_EmissaoDoc', namespace)
    vl_TotalDoc = root.find('.//ptuA500:vl_TotalDoc', namespace)
    
    if nr_Documento is not None:
        nr_Documento = nr_Documento.text
    else:
        nr_Documento = None
    
    if dt_EmissaoDoc is not None:
        dt_EmissaoDoc = dt_EmissaoDoc.text
    else:
        dt_EmissaoDoc = None
    
    if vl_TotalDoc is not None:
        vl_TotalDoc = vl_TotalDoc.text
    else:
        vl_TotalDoc = None
    
    return nr_Documento, dt_EmissaoDoc, vl_TotalDoc

# Função para verificar se as informações do XML existem no PDF usando pdfplumber
def verificar_info_no_pdf(arquivo_pdf, info_xml):
    with pdfplumber.open(arquivo_pdf) as pdf:
        pdf_text = ""
        for page in pdf.pages:
            pdf_text += page.extract_text()
    resultados = []
    
    for info in info_xml:
        if info is None:
            resultados.append("Não encontrada")
        elif info in pdf_text:
            resultados.append(info)
        else:
            resultados.append("Não encontrada")
    
    return resultados

# Função para extrair arquivos XML e PDF de um arquivo ZIP
def extrair_xml_e_pdf_de_zip(arquivo_zip, pasta_destino):
    with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            zip_ref.extract(file_info, pasta_destino)


janela = Tk()
janela.withdraw()
janela.attributes("-topmost", True) # Manter no topo
diretorio_raiz = askdirectory(title="Selecionar Pasta dos Arquivos ZIP")
janela.destroy()

#Dir arquivo ZIP
for pasta_raiz, _, arquivos in os.walk(diretorio_raiz):
    for arquivo in arquivos:
        if arquivo.endswith('.zip'):
            arquivo_zip = os.path.join(pasta_raiz, arquivo)
            pasta_destino = os.path.join(pasta_raiz, 'temp')  # Pasta temporária para extrair XML e PDF
            os.makedirs(pasta_destino, exist_ok=True)
            
            # Extrair XML e PDF do arquivo ZIP
            extrair_xml_e_pdf_de_zip(arquivo_zip, pasta_destino)
            
            #Dir arquivo XML
            for arquivo in os.listdir(pasta_destino):
                extensao = arquivo.split(".")[1]
                if extensao.isdigit():
                    arquivo_xml = os.path.join(pasta_destino, arquivo)
                    nr_Documento, dt_EmissaoDoc, vl_TotalDoc = extrair_info_xml(arquivo_xml)
                    
                    #Dir arquivo PDF
                    for arquivo in os.listdir(pasta_destino):
                
                        if arquivo.startswith(f"{'N'+str(extensao)+str(nr_Documento)}_"):
                                
                            arquivo_pdf = os.path.join(pasta_destino, arquivo)
                            #print(arquivo, nr_Documento, dt_EmissaoDoc, vl_TotalDoc)
                            if os.path.exists(arquivo_pdf):
                                try:
                                    dt_EmissaoDoc = datetime.strptime(dt_EmissaoDoc, "%Y%m%d")
                                except:
                                    dt_EmissaoDoc = datetime.strptime(dt_EmissaoDoc, "%d/%m/%Y")
                                dt_EmissaoDoc = dt_EmissaoDoc.strftime("%d/%m/%Y")
                                try:
                                    vl_TotalDoc = locale.currency(float(vl_TotalDoc), grouping=True)
                                except:
                                    try:
                                        vl_TotalDoc = vl_TotalDoc.replace(',','.')
                                        vl_TotalDoc = locale.currency(float(vl_TotalDoc), grouping=True)
                                    except:
                                        vl_TotalDoc = vl_TotalDoc.replace('.', '', 1).replace('.', '.')
                                        vl_TotalDoc = locale.currency(float(vl_TotalDoc), grouping=True)

                                
                                vl_TotalDoc = vl_TotalDoc.replace('R$ ','')
                                info_xml = [nr_Documento, dt_EmissaoDoc, vl_TotalDoc]
                                
                                resultados = verificar_info_no_pdf(arquivo_pdf, info_xml)
                            
                                if "Não encontrada" in resultados or "Tag não encontrada" in resultados:
                                    if resultados[1] != dt_EmissaoDoc or  resultados[2] != vl_TotalDoc:
                                        print(f'Arquivo XML: {arquivo_xml}')
                                        print(f'Arquivo PDF: {arquivo_pdf}')
                                        print(f'Data de Emissão: {resultados[1]} | Resultado Esperado: {dt_EmissaoDoc}')
                                        print(f'Valor Total: {resultados[2]} | Resultado Esperado: {vl_TotalDoc}')
                                        print('-' * 60)
                         
                                    
                                  
            # Remova a pasta temporária após o processamento
            for file in os.listdir(pasta_destino):
                file_path = os.path.join(pasta_destino, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            os.rmdir(pasta_destino)
input()
