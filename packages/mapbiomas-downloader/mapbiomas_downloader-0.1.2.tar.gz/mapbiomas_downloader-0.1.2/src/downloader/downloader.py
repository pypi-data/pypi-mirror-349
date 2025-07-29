# src/downloader/downloader.py
# Author: Ricardo Malnati

"""
Este módulo contém as funções principais para o download de arquivos GeoTIFF do MapBiomas.
"""
from enum import Enum
from typing import Dict, List, Optional
import json
import os
import importlib.resources
import asyncio
import logging
from playwright.async_api import async_playwright, Download, Page
import time
import pandas as pd


class State(str, Enum):
    """
    Enumeration representing states in Brazil.
    """
    AC = "AC"
    AL = "AL"
    AM = "AM"
    AP = "AP"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MG = "MG"
    MS = "MS"
    MT = "MT"
    PA = "PA"
    PB = "PB"
    PE = "PE"
    PI = "PI"
    PR = "PR"
    RJ = "RJ"
    RN = "RN"
    RO = "RO"
    RR = "RR"
    RS = "RS"
    SC = "SC"
    SE = "SE"
    SP = "SP"
    TO = "TO"


class Downloader:
    """
    Classe responsável por realizar o download dos arquivos GeoTIFF.
    """
    
    # Dicionário de códigos de UF do IBGE
    __state_codes: Dict[str, str] = {
        "AC": "12", "AL": "27", "AM": "13", "AP": "16", "BA": "29",
        "CE": "23", "DF": "53", "ES": "32", "GO": "52", "MA": "21",
        "MG": "31", "MS": "50", "MT": "51", "PA": "15", "PB": "25",
        "PE": "26", "PI": "22", "PR": "41", "RJ": "33", "RN": "24",
        "RO": "11", "RR": "14", "RS": "43", "SC": "42", "SE": "28",
        "SP": "35", "TO": "17"
    }
    
    # Cache para armazenar os dados das cidades
    __cities_data = None

    @staticmethod
    def __load_cities_from_csv():
        """
        Carrega os dados das cidades a partir do arquivo TABMUN.csv
        
        Returns:
            Dict[str, dict]: Dicionário com os dados das cidades, indexado pelo código IBGE
        """
        if Downloader.__cities_data is not None:
            return Downloader.__cities_data
            
        try:
            # Caminho do arquivo CSV relativo à raiz do projeto
            csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'TABMUN.csv')
            
            # Carrega o CSV como DataFrame
            df = pd.read_csv(csv_path, sep=';', header=None, 
                             encoding='latin-1', 
                             names=['cod_nacional', 'cnpj', 'nome', 'uf', 'ibge'],
                             dtype={'ibge': str})
            
            # Converte o DataFrame para um dicionário
            cities_dict = {}
            for _, row in df.iterrows():
                if row['ibge'] and len(str(row['ibge'])) == 7:
                    cities_dict[row['ibge']] = {
                        "ibge": row['ibge'],
                        "nome": row['nome'].strip(),
                        "uf": row['uf'].strip()
                    }
            
            Downloader.__cities_data = cities_dict
            return cities_dict
        except Exception as e:
            logging.error(f"Erro ao carregar dados de TABMUN.csv: {e}")
            # Dados mínimos de fallback para não quebrar o código
            return {
                "3550308": {"ibge": "3550308", "nome": "São Paulo", "uf": "SP"},
                "3304557": {"ibge": "3304557", "nome": "Rio de Janeiro", "uf": "RJ"},
                "3106200": {"ibge": "3106200", "nome": "Belo Horizonte", "uf": "MG"},
                "5300108": {"ibge": "5300108", "nome": "Brasília", "uf": "DF"}
            }

    @staticmethod
    def get_state_code(state: str) -> str:
        """
        Retorna o código IBGE de um estado dado o nome ou sigla.
        
        Args:
            state: Sigla do estado (UF)
            
        Returns:
            Código IBGE do estado ou string vazia se não encontrado
        """
        return Downloader.__state_codes.get(state.upper(), "")

    @staticmethod
    def is_valid_state(state: str) -> bool:
        """
        Verifica se o estado fornecido é válido.
        
        Args:
            state: Sigla do estado (UF)
            
        Returns:
            True se o estado for válido, False caso contrário
        """
        return state.upper() in Downloader.__state_codes

    @staticmethod
    def get_city_info(city_code: str) -> dict:
        """
        Retorna informações de uma cidade dado o seu código IBGE.
        
        Args:
            city_code: Código IBGE da cidade (7 dígitos)
            
        Returns:
            Dicionário com informações da cidade ou dicionário vazio se não encontrado
        """
        try:
            # Tenta usar o pacote cidade_ibge_tom se estiver disponível
            from cidade_ibge_tom import info_cidade
            return info_cidade(codigo=city_code)
        except ImportError:
            # Usa dados do arquivo TABMUN.csv se o pacote não estiver disponível
            cities_data = Downloader.__load_cities_from_csv()
            return cities_data.get(city_code, {})

    @staticmethod
    def get_cities_by_state(state_code: str) -> list:
        """
        Retorna uma lista de cidades de um estado dado o código IBGE do estado.
        
        Args:
            state_code: Código ou sigla do estado
            
        Returns:
            Lista de dicionários com informações das cidades do estado
        """
        # Se for passada a sigla UF, converte para código
        original_state = state_code
        if len(state_code) == 2:
            state_code = Downloader.get_state_code(state_code)
            
        if not state_code:
            return []
        
        try:
            # Tenta usar o pacote cidade_ibge_tom se estiver disponível
            try:
                with importlib.resources.open_text("cidade_ibge_tom", "lista_cidades.json") as f:
                    cities = json.load(f)
            except (ImportError, FileNotFoundError):
                # Usa dados do arquivo TABMUN.csv
                cities_data = Downloader.__load_cities_from_csv()
                cities = list(cities_data.values())
                
            # Filtra as cidades pelo estado, seja pelo código IBGE ou pela sigla UF
            return [city for city in cities if 
                    (city["ibge"].startswith(state_code) if state_code.isdigit() else 
                     city["uf"] == original_state.upper())]
        except Exception as e:
            logging.error(f"Erro ao buscar cidades por estado: {e}")
            return []

    @staticmethod
    def is_valid_city_code(city_code: str) -> bool:
        """
        Verifica se o código IBGE da cidade é válido.
        
        Args:
            city_code: Código IBGE da cidade (7 dígitos)
            
        Returns:
            True se o código for válido, False caso contrário
        """
        if not city_code or not city_code.isdigit() or len(city_code) != 7:
            return False
        city_info = Downloader.get_city_info(city_code)
        return bool(city_info)


async def baixar_mapbiomas_por_municipio(
    codigo_municipio: str,
    ano_inicio: int = 1985,
    ano_fim: int = 2023,
    diretorio_saida: Optional[str] = None
) -> List[str]:
    """
    Baixa arquivos GeoTIFF do MapBiomas para um município específico.
    
    Args:
        codigo_municipio: Código IBGE do município (7 dígitos)
        ano_inicio: Ano inicial para baixar (padrão: 1985)
        ano_fim: Ano final para baixar (padrão: 2023)
        diretorio_saida: Diretório onde os arquivos serão salvos
                        (padrão: downloads_mapbiomas/<codigo_municipio>)
    
    Returns:
        Lista de caminhos dos arquivos baixados
    """
    # Configura o log
    log_path = os.path.join(os.path.dirname(__file__), "mapbiomas_download.log")
    logging.basicConfig(
        filename=log_path, 
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    # Valida o código do município
    if not Downloader.is_valid_city_code(codigo_municipio):
        erro_msg = f"Código de município inválido: {codigo_municipio}"
        logging.error(erro_msg)
        raise ValueError(erro_msg)
    
    # Obtém informações do município
    info_municipio = Downloader.get_city_info(codigo_municipio)
    nome_municipio = info_municipio.get('nome', 'desconhecido')
    
    # Define o diretório de saída
    if not diretorio_saida:
        diretorio_saida = os.path.join("downloads_mapbiomas", codigo_municipio)
    
    # Cria o diretório se não existir
    os.makedirs(diretorio_saida, exist_ok=True)
    
    arquivos_baixados = []
    
    logging.info(f"Iniciando download para {nome_municipio} ({codigo_municipio}) anos {ano_inicio}-{ano_fim}")
    print(f"🌍 Iniciando download para {nome_municipio} ({codigo_municipio})")
    print(f"📅 Anos: {ano_inicio} a {ano_fim}")
    print(f"📂 Diretório: {diretorio_saida}")
    
    # Configura o Playwright e inicia downloads
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        
        for ano in range(ano_inicio, ano_fim + 1):
            # URL base do MapBiomas para o Brasil (Collection 9)
            url = f"https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_9/lclu/coverage/brasil_coverage_{ano}.tif"
            
            # Nome do arquivo de saída incluindo o código do município
            nome_arquivo = f"{codigo_municipio}_mapbiomas_{ano}.tif"
            caminho_arquivo = os.path.join(diretorio_saida, nome_arquivo)
            
            logging.info(f"Tentando baixar: {url}")
            print(f"⬇️  Baixando dados de {ano}...")
            
            try:
                await page.goto(url)
                
                # Aguarda o download iniciar
                download = await page.wait_for_event("download", timeout=60000)
                
                # Salva o arquivo no diretório especificado
                await download.save_as(caminho_arquivo)
                
                arquivos_baixados.append(caminho_arquivo)
                logging.info(f"Download concluído: {caminho_arquivo}")
                print(f"✅ Arquivo salvo: {nome_arquivo}")
                
            except Exception as e:
                logging.error(f"Erro ao baixar dados de {ano}: {e}")
                print(f"❌ Erro ao baixar dados de {ano}: {e}")
        
        await browser.close()
    
    return arquivos_baixados


async def baixar_mapbiomas_por_estado(
    uf: str,
    ano_inicio: int = 1985,
    ano_fim: int = 2023,
    diretorio_base: str = "downloads_mapbiomas"
) -> dict:
    """
    Baixa arquivos do MapBiomas para todos os municípios de um estado.
    
    Args:
        uf: Sigla do estado (UF)
        ano_inicio: Ano inicial para baixar
        ano_fim: Ano final para baixar
        diretorio_base: Diretório base para armazenar os downloads
    
    Returns:
        Dicionário com status dos downloads por município
    """
    # Configura o log
    log_path = os.path.join(os.path.dirname(__file__), "mapbiomas_download.log")
    logging.basicConfig(
        filename=log_path, 
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    if not Downloader.is_valid_state(uf):
        raise ValueError(f"UF inválida: {uf}")
    
    # Obtém a lista de municípios do estado
    municipios = Downloader.get_cities_by_state(uf)
    
    if not municipios:
        logging.warning(f"Nenhum município encontrado para o estado {uf}")
        return {}
    
    resultados = {}
    
    print(f"🏙️  Encontrados {len(municipios)} municípios no estado {uf}")
    
    # Cria diretório para o estado
    diretorio_estado = os.path.join(diretorio_base, uf)
    os.makedirs(diretorio_estado, exist_ok=True)
    
    # Processa cada município
    for i, municipio in enumerate(municipios, 1):
        codigo = municipio["ibge"]
        nome = municipio["nome"]
        
        print(f"\n[{i}/{len(municipios)}] Processando {nome} ({codigo})")
        
        diretorio_municipio = os.path.join(diretorio_estado, codigo)
        
        try:
            arquivos = await baixar_mapbiomas_por_municipio(
                codigo_municipio=codigo,
                ano_inicio=ano_inicio,
                ano_fim=ano_fim,
                diretorio_saida=diretorio_municipio
            )
            resultados[codigo] = {
                "status": "sucesso",
                "arquivos": len(arquivos),
                "nome": nome
            }
        except Exception as e:
            logging.error(f"Falha ao processar município {codigo}: {e}")
            resultados[codigo] = {
                "status": "erro",
                "mensagem": str(e),
                "nome": nome
            }
    
    return resultados


async def main():
    """
    Função principal para execução do script.
    Processa os argumentos da linha de comando e inicia os downloads.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ferramenta para download de arquivos GeoTIFF do MapBiomas para municípios ou estados brasileiros",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python -m src.downloader.downloader --municipio 3550308 --ano-inicio 2020 --ano-fim 2021
  python -m src.downloader.downloader --estado SP --ano-inicio 2022 --ano-fim 2022
  python -m src.downloader.downloader --teste
  python -m src.downloader.downloader --publicar

Valores padrão se não especificados:
  - Ano inicial: 1985
  - Ano final: 2023
  - Diretório de saída: ./downloads_mapbiomas/<municipio ou estado>

Fonte de dados:
  - Os dados de municípios são lidos do arquivo TABMUN.csv
  - Collection 9 do MapBiomas
"""
    )
    
    grupo_dados = parser.add_argument_group('Opções de download')
    grupo_dados.add_argument("--municipio", "-m", help="Código IBGE do município (7 dígitos)")
    grupo_dados.add_argument("--estado", "-e", help="Sigla do estado (UF)")
    grupo_dados.add_argument("--ano-inicio", "-i", type=int, default=1985, help="Ano inicial (padrão: 1985)")
    grupo_dados.add_argument("--ano-fim", "-f", type=int, default=2023, help="Ano final (padrão: 2023)")
    grupo_dados.add_argument("--diretorio", "-d", default="downloads_mapbiomas", help="Diretório base para os arquivos baixados")
    
    grupo_operacoes = parser.add_argument_group('Outras operações')
    grupo_operacoes.add_argument("--teste", "-t", action="store_true", help="Executa os testes automatizados")
    grupo_operacoes.add_argument("--publicar", "-p", action="store_true", help="Prepara e publica o pacote no PyPI")
    
    args = parser.parse_args()
    
    # Executar testes
    if args.teste:
        import subprocess
        import sys
        
        print("🧪 Executando testes automatizados...")
        try:
            resultado = subprocess.run(["pytest", "-xvs"], check=True)
            if resultado.returncode == 0:
                print("✅ Todos os testes passaram com sucesso!")
            else:
                print("❌ Falha em alguns testes.")
                return
        except subprocess.CalledProcessError:
            print("❌ Erro ao executar os testes.")
            return
        except FileNotFoundError:
            print("❌ Pytest não encontrado. Instale com 'pip install pytest'.")
            return
        return
    
    # Publicar pacote
    if args.publicar:
        import subprocess
        import sys
        
        print("📦 Preparando pacote para publicação...")
        try:
            print("🧹 Limpando diretórios de build anteriores...")
            subprocess.run(["rm", "-rf", "dist", "build", "*.egg-info"], check=False)
            
            print("🔨 Construindo pacote...")
            subprocess.run(["python", "-m", "build"], check=True)
            
            print("🚀 Publicando no PyPI...")
            subprocess.run(["python", "-m", "twine", "upload", "dist/*"], check=True)
            
            print("✅ Publicação concluída com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao publicar pacote: {e}")
            return
        return
    
    # Verifica se foi especificado pelo menos um município ou estado
    if not args.municipio and not args.estado:
        print("⚠️  É necessário especificar um município (--municipio) ou um estado (--estado)")
        print("ℹ️  Use --help para ver todas as opções disponíveis")
        return
    
    # Processa por município
    if args.municipio:
        try:
            await baixar_mapbiomas_por_municipio(
                codigo_municipio=args.municipio,
                ano_inicio=args.ano_inicio,
                ano_fim=args.ano_fim,
                diretorio_saida=os.path.join(args.diretorio, args.municipio)
            )
        except Exception as e:
            logging.error(f"Erro ao processar município {args.municipio}: {e}")
            print(f"❌ Erro: {e}")
    
    # Processa por estado
    if args.estado:
        try:
            resultados = await baixar_mapbiomas_por_estado(
                uf=args.estado,
                ano_inicio=args.ano_inicio,
                ano_fim=args.ano_fim,
                diretorio_base=args.diretorio
            )
            
            # Imprime resumo
            sucessos = sum(1 for r in resultados.values() if r["status"] == "sucesso")
            print(f"\n📊 Resumo do processamento para {args.estado}:")
            print(f"   ✅ Municípios processados com sucesso: {sucessos}")
            print(f"   ❌ Falhas: {len(resultados) - sucessos}")
            
        except Exception as e:
            logging.error(f"Erro ao processar estado {args.estado}: {e}")
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 