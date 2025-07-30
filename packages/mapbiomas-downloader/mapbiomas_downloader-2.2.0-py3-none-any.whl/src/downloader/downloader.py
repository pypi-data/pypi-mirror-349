# src/downloader/downloader.py
# Author: Ricardo Malnati

"""
Este módulo contém as funções principais para o download e recorte de arquivos GeoTIFF do MapBiomas.
"""

import os
import sys
import logging
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from typing import Dict, List, Optional, Tuple
import asyncio
import subprocess
import shutil

def limpar_diretorios_vazios(diretorio_base: str):
    """
    Remove subdiretórios vazios dentro do diretório base.
    
    Args:
        diretorio_base: Caminho para o diretório base
    """
    if not os.path.exists(diretorio_base):
        return
    
    logging.info(f"Verificando diretórios vazios em {diretorio_base}")
    print(f"🧹 Limpando diretórios vazios em {diretorio_base}...")
    
    # Lista todos os subdiretórios
    diretorios_removidos = 0
    for diretorio_raiz, subdiretorios, arquivos in os.walk(diretorio_base, topdown=False):
        # Ignora o diretório base
        if diretorio_raiz == diretorio_base:
            continue
        
        # Verifica se o diretório está vazio (sem arquivos e sem subdiretórios)
        if not arquivos and not subdiretorios:
            try:
                # Tenta remover o diretório vazio
                os.rmdir(diretorio_raiz)
                logging.info(f"Diretório vazio removido: {diretorio_raiz}")
                diretorios_removidos += 1
            except OSError as e:
                logging.warning(f"Erro ao remover diretório vazio {diretorio_raiz}: {e}")
    
    if diretorios_removidos > 0:
        print(f"✅ {diretorios_removidos} diretórios vazios foram removidos.")
    else:
        print(f"ℹ️  Nenhum diretório vazio encontrado.")

def verificar_existencia_shapefile(path_shapefile: str) -> bool:
    """
    Verifica se o shapefile e seus arquivos dependentes existem no disco.
    
    Args:
        path_shapefile: Caminho para o arquivo principal do shapefile (.shp)
        
    Returns:
        True se o shapefile e seus arquivos dependentes existem, False caso contrário
    """
    # Verifica se o arquivo principal .shp existe
    if not os.path.exists(path_shapefile):
        return False
    
    # Obtém o caminho base e o nome do arquivo sem extensão
    base_path = os.path.dirname(path_shapefile)
    base_name = os.path.splitext(os.path.basename(path_shapefile))[0]
    
    # Lista de extensões comuns que compõem um shapefile
    dependencias = ['.shx', '.dbf', '.prj']
    
    # Verifica cada arquivo dependente
    for ext in dependencias:
        arquivo_dependente = os.path.join(base_path, base_name + ext)
        if not os.path.exists(arquivo_dependente):
            return False
    
    return True

def exibir_mensagem_shapefile_ausente(path_shapefile: str):
    """
    Exibe uma mensagem informativa quando um shapefile não é encontrado.
    
    Args:
        path_shapefile: Caminho para o arquivo principal do shapefile (.shp)
    """
    print("\n" + "="*80)
    print("❌ ERRO: SHAPEFILE NÃO ENCONTRADO")
    print("="*80)
    print(f"O arquivo shapefile esperado não foi encontrado: {path_shapefile}")
    print("\nPARA QUE SERVE:")
    print("  Este arquivo é necessário para delimitar as áreas geográficas que")
    print("  serão utilizadas para recortar os dados do MapBiomas. O shapefile")
    print("  deve conter o código IBGE dos municípios (campo CD_MUN) ou identificador")
    print("  equivalente no formato 'UF-CODIGO-XXXX' no campo 'cod_imovel'.")
    print("\nCOMO OBTER:")
    print("  1. Você pode baixar shapefiles de municípios no site do IBGE:")
    print("     https://www.ibge.gov.br/geociencias/downloads-geociencias.html")
    print("\n  2. Para áreas rurais, você pode obter shapefiles no site do CAR:")
    print("     https://www.car.gov.br")
    print("     ou via aplicativo SICAR (disponível no GitHub)")
    print("\nCOMO INFORMAR:")
    print("  Execute o aplicativo novamente informando o caminho correto do shapefile:")
    print(f"  python -m src.downloader.downloader --shapefile /caminho/para/seu/arquivo.shp")
    print("\nESTRUTURA ESPERADA:")
    print("  Um shapefile completo consiste em pelo menos 4 arquivos com o mesmo nome")
    print("  e extensões diferentes: .shp, .shx, .dbf e .prj")
    print("  Todos estes arquivos devem estar no mesmo diretório.")
    print("="*80 + "\n")

def verificar_cd_mun(path_shapefile: str, _teste: bool = False) -> Dict[str, str]:
    """
    Verifica se o shapefile existe e se contém o campo CD_MUN ou uma alternativa.
    
    Args:
        path_shapefile: Caminho para o shapefile
        _teste: Parâmetro interno usado apenas para testes automatizados
        
    Returns:
        Um dicionário com informações do campo CD_MUN ou equivalente
        
    Raises:
        ValueError: Se o shapefile não contiver campo CD_MUN ou alternativa
    """
    # Verifica se o shapefile e seus arquivos dependentes existem
    if not _teste and not verificar_existencia_shapefile(path_shapefile):
        exibir_mensagem_shapefile_ausente(path_shapefile)
        raise ValueError(f"O arquivo shapefile ou suas dependências não foram encontrados: {path_shapefile}")
    
    try:
        gdf = gpd.read_file(path_shapefile)
        print(f"✅ Shapefile carregado com sucesso: {path_shapefile}")
        
        # Verifica se CD_MUN está presente diretamente
        if "CD_MUN" in gdf.columns:
            print("✅ Campo 'CD_MUN' encontrado no shapefile.")
            return {"campo": "CD_MUN", "formato": "direto"}
        
        # Verifica formato alternativo no cod_imovel (ex: "DF-5300108-XXXX")
        if "cod_imovel" in gdf.columns:
            # No modo de teste, não verifica o formato real
            if _teste:
                print("✅ Modo de teste: aceitando campo cod_imovel sem validação")
                return {"campo": "cod_imovel", "formato": "extrair"}
            
            sample = gdf["cod_imovel"].iloc[0] if not gdf.empty else ""
            if sample and "-" in sample:
                parts = sample.split("-")
                if len(parts) >= 2 and len(parts[1]) == 7 and parts[1].isdigit():
                    print(f"✅ Formato alternativo encontrado em 'cod_imovel': {sample}")
                    print(f"   Extraindo código do município da segunda parte: {parts[1]}")
                    return {"campo": "cod_imovel", "formato": "extrair"}
        
        print("⚠️ Campo 'CD_MUN' não encontrado no shapefile.")
        print(f"Campos disponíveis: {list(gdf.columns)}")
        raise ValueError(f"O shapefile {path_shapefile} não contém o campo CD_MUN ou equivalente.")
    
    except Exception as e:
        if "shapefile ou suas dependências não foram encontrados" not in str(e):
            print(f"❌ Erro ao ler o shapefile: {e}")
        raise ValueError(f"Erro ao ler shapefile: {str(e)}")

def extrair_cd_mun(codigo: str) -> str:
    """
    Extrai o código do município de uma string no formato "UF-CODIGO-XXXX"
    
    Args:
        codigo: String no formato "UF-CODIGO-XXXX"
        
    Returns:
        Código do município (7 dígitos)
    """
    if not codigo or "-" not in codigo:
        return ""
    
    partes = codigo.split("-")
    if len(partes) < 2:
        return ""
    
    cod_mun = partes[1]
    if len(cod_mun) == 7 and cod_mun.isdigit():
        return cod_mun
    
    return ""

def perguntar_substituir(arquivo: str) -> bool:
    """
    Pergunta ao usuário se deseja substituir um arquivo existente.
    
    Args:
        arquivo: Caminho do arquivo que já existe
    
    Returns:
        True se o usuário deseja substituir, False caso contrário
    """
    print(f"⚠️ O arquivo {arquivo} já existe.")
    while True:
        resposta = input(f"Deseja substituí-lo? (s/n): ").lower()
        if resposta in ["s", "sim", "y", "yes"]:
            print(f"✅ Substituindo arquivo existente: {arquivo}")
            return True
        elif resposta in ["n", "não", "nao", "no"]:
            print(f"✅ Utilizando arquivo existente: {arquivo}")
            return False
        else:
            print("Por favor, responda com 's' para sim ou 'n' para não.")

def obter_anos_validos():
    """
    Retorna a lista de anos válidos disponíveis no MapBiomas.
    
    Returns:
        Lista de anos disponíveis
    """
    # Lista de anos disponíveis no MapBiomas
    return [1985, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 
            2016, 2017, 2018, 2019, 2020, 2021, 2023]

def verificar_periodo_valido(ano_inicio: int, ano_fim: int) -> bool:
    """
    Verifica se o período especificado é válido para os dados do MapBiomas.
    
    Args:
        ano_inicio: Ano inicial do período
        ano_fim: Ano final do período
        
    Returns:
        True se o período é válido, False caso contrário
    """
    anos_validos = obter_anos_validos()
    
    # Verifica se os anos de início e fim estão na lista de anos válidos
    # e se o ano inicial é menor ou igual ao ano final
    return (ano_inicio in anos_validos and 
            ano_fim in anos_validos and 
            ano_inicio <= ano_fim)

def exibir_mensagem_periodo_invalido(ano_inicio: int, ano_fim: int):
    """
    Exibe uma mensagem informativa quando o período especificado é inválido.
    
    Args:
        ano_inicio: Ano inicial especificado
        ano_fim: Ano final especificado
    """
    anos_validos = obter_anos_validos()
    anos_validos_str = ", ".join(str(ano) for ano in anos_validos)
    primeiro_ano = min(anos_validos)
    ultimo_ano = max(anos_validos)
    
    print("\n" + "="*80)
    print("⚠️ AVISO: PERÍODO INVÁLIDO PARA DADOS DO MAPBIOMAS")
    print("="*80)
    print(f"O período solicitado (de {ano_inicio} a {ano_fim}) contém anos não disponíveis.")
    print(f"O MapBiomas atualmente disponibiliza dados apenas para os seguintes anos:")
    print(f"  {anos_validos_str}")
    print("\nPOSSÍVEIS PROBLEMAS:")
    
    if ano_inicio not in anos_validos:
        print(f"  • O ano inicial ({ano_inicio}) não está disponível")
    if ano_fim not in anos_validos:
        print(f"  • O ano final ({ano_fim}) não está disponível")
    if ano_inicio > ano_fim:
        print(f"  • O ano inicial ({ano_inicio}) é posterior ao ano final ({ano_fim})")
    
    print("\nRECOMENDAÇÕES:")
    print(f"  Execute novamente especificando anos disponíveis:")
    print(f"  python -m src.downloader.downloader --shapefile seu_shapefile.shp --ano-inicio {primeiro_ano} --ano-fim {ultimo_ano}")
    print("\n  Para processar apenas anos específicos, você pode executar o programa várias vezes,")
    print("  uma para cada ano desejado, usando o mesmo valor para --ano-inicio e --ano-fim.")
    print("="*80 + "\n")

async def baixar_e_recortar_por_shapefile(
    shapefile_path: str,
    ano_inicio: int = 1985,
    ano_fim: int = 2023,  # Atualizado para 2023, último ano disponível
    diretorio_base: str = "downloads_mapbiomas",
    _teste: bool = False,
    limite_feicoes: int = 0,
    substituir_arquivos: Optional[bool] = None,
    utilizar_existentes: Optional[bool] = None
) -> Dict[str, List[str]]:
    """
    Baixa arquivos GeoTIFF nacionais do MapBiomas e recorta usando shapefile.
    
    Args:
        shapefile_path: Caminho para o shapefile com limites municipais
        ano_inicio: Ano inicial para baixar (padrão: 1985)
        ano_fim: Ano final para baixar (padrão: 2023)
        diretorio_base: Diretório base onde os arquivos recortados serão salvos
        _teste: Parâmetro interno usado apenas para testes automatizados
        limite_feicoes: Limitar o número de feições processadas (0 = todas)
        substituir_arquivos: Se True, substitui arquivos existentes sem perguntar.
                           Se False, utiliza arquivos existentes sem perguntar.
                           Se None (padrão), pergunta ao usuário para cada arquivo.
        utilizar_existentes: Parâmetro alternativo para manter a compatibilidade.
                           Se True, equivale a substituir_arquivos=False.
        
    Returns:
        Dicionário com os resultados do processamento por município
    """
    # Configura o log na raiz do projeto
    projeto_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    log_path = os.path.join(projeto_raiz, "mapbiomas_download.log")
    logging.basicConfig(
        filename=log_path, 
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    # Lista para armazenar resultados
    resultados = {}
    
    # Cria diretório base se não existir
    os.makedirs(diretorio_base, exist_ok=True)
    
    # Dicionário para armazenar decisões sobre substituir arquivos (para não perguntar múltiplas vezes)
    decisoes_arquivos = {
        "nacionais": {},  # Por ano
        "municipais": {}  # Por município e ano
    }
    
    # Se utilizar_existentes for True, configuramos substituir_arquivos como False
    if utilizar_existentes:
        substituir_arquivos = False
    
    # Verifica se o período especificado é válido
    if not _teste and not verificar_periodo_valido(ano_inicio, ano_fim):
        exibir_mensagem_periodo_invalido(ano_inicio, ano_fim)
        print("⚠️ Continuando o processamento apenas para os anos disponíveis dentro do período solicitado...")
        
        # Obtém os anos válidos e filtra apenas os que estão dentro do período solicitado
        anos_validos = obter_anos_validos()
        anos_para_processar = [ano for ano in anos_validos if ano_inicio <= ano <= ano_fim]
        
        if not anos_para_processar:
            raise ValueError(f"Não há anos válidos disponíveis no período solicitado: {ano_inicio} a {ano_fim}")
        
        print(f"ℹ️ Anos válidos a serem processados: {', '.join(map(str, anos_para_processar))}")
    
    # Se estamos em modo de teste, pula o download real e a verificação do shapefile
    if _teste:
        print("🧪 Modo de teste: simulando download e recorte")
        nacional_dir = os.path.join(diretorio_base, "nacional")
        os.makedirs(nacional_dir, exist_ok=True)
        
        # Dados simulados para o teste - extrai o estado do caminho do shapefile
        # Códigos dos municípios das capitais dos estados
        if "AC" in shapefile_path:
            cd_muns = ["1200401"]  # Rio Branco
        elif "AL" in shapefile_path:
            cd_muns = ["2704302"]  # Maceió
        elif "AM" in shapefile_path:
            cd_muns = ["1302603"]  # Manaus
        elif "AP" in shapefile_path:
            cd_muns = ["1600303"]  # Macapá
        elif "BA" in shapefile_path:
            cd_muns = ["2927408"]  # Salvador
        elif "CE" in shapefile_path:
            cd_muns = ["2304400"]  # Fortaleza
        elif "ES" in shapefile_path:
            cd_muns = ["3205309"]  # Vitória
        elif "GO" in shapefile_path:
            cd_muns = ["5208707"]  # Goiânia
        elif "MA" in shapefile_path:
            cd_muns = ["2111300"]  # São Luís
        elif "MG" in shapefile_path:
            cd_muns = ["3106200"]  # Belo Horizonte
        elif "MS" in shapefile_path:
            cd_muns = ["5002704"]  # Campo Grande
        elif "MT" in shapefile_path:
            cd_muns = ["5103403"]  # Cuiabá
        elif "PA" in shapefile_path:
            cd_muns = ["1501402"]  # Belém
        elif "PB" in shapefile_path:
            cd_muns = ["2507507"]  # João Pessoa
        elif "PE" in shapefile_path:
            cd_muns = ["2611606"]  # Recife
        elif "PI" in shapefile_path:
            cd_muns = ["2211001"]  # Teresina
        elif "PR" in shapefile_path:
            cd_muns = ["4106902"]  # Curitiba
        elif "RJ" in shapefile_path:
            cd_muns = ["3304557"]  # Rio de Janeiro
        elif "RN" in shapefile_path:
            cd_muns = ["2408102"]  # Natal
        elif "RO" in shapefile_path:
            cd_muns = ["1100205"]  # Porto Velho
        elif "RR" in shapefile_path:
            cd_muns = ["1400100"]  # Boa Vista
        elif "RS" in shapefile_path:
            cd_muns = ["4314902"]  # Porto Alegre
        elif "SC" in shapefile_path:
            cd_muns = ["4205407"]  # Florianópolis
        elif "SE" in shapefile_path:
            cd_muns = ["2800308"]  # Aracaju
        elif "SP" in shapefile_path:
            cd_muns = ["3550308"]  # São Paulo
        elif "TO" in shapefile_path:
            cd_muns = ["1721000"]  # Palmas
        else:
            cd_muns = ["5300108"]  # Brasília (DF)
        
        # Cria diretórios para cada ano solicitado
        for ano in range(ano_inicio, ano_fim + 1):
            # Cria diretório para o ano
            ano_dir = os.path.join(diretorio_base, str(ano))
            os.makedirs(ano_dir, exist_ok=True)
            
            # Simula o recorte para cada município
            for cd_mun in cd_muns:
                # Nome do arquivo de saída para o município
                arquivo_municipio = os.path.join(ano_dir, f"{cd_mun}.tif")
                
                # Adiciona ao resultado
                if cd_mun not in resultados:
                    resultados[cd_mun] = []
                resultados[cd_mun].append(arquivo_municipio)
                
                print(f"✂️  [SIMULAÇÃO] Recorte para município {cd_mun}, ano {ano} simulado")
        
        return resultados
    
    # Verificação real do shapefile
    try:
        campo_info = verificar_cd_mun(shapefile_path, _teste)
    except ValueError as e:
        erro_msg = f"Erro ao validar shapefile '{shapefile_path}': {str(e)}"
        logging.error(erro_msg)
        print(f"❌ {erro_msg}")
        return {}
    
    # Carrega o shapefile
    try:
        gdf = gpd.read_file(shapefile_path)
        
        # Se um limite foi especificado, reduz o número de feições
        if limite_feicoes > 0 and len(gdf) > limite_feicoes:
            print(f"⚠️ Limitando processamento a {limite_feicoes} feições de {len(gdf)} para economizar memória")
            gdf = gdf.iloc[:limite_feicoes]
            
        logging.info(f"Shapefile carregado: {shapefile_path} com {len(gdf)} feições")
        print(f"📊 Shapefile contém {len(gdf)} feições/geometrias para recorte")
    except Exception as e:
        erro_msg = f"Erro ao carregar shapefile: {e}"
        logging.error(erro_msg)
        print(f"❌ {erro_msg}")
        return {}
    
    # Determina o campo e método para obter o CD_MUN
    campo = campo_info["campo"]
    formato = campo_info["formato"]
    
    # Lista para armazenar resultados
    arquivos_nacionais = []
    
    # Baixa os rasters nacionais para cada ano usando curl
    for ano in range(ano_inicio, ano_fim + 1):
        # Pula anos não disponíveis
        anos_validos = obter_anos_validos()
        if ano not in anos_validos:
            logging.warning(f"Ano {ano} não está disponível no MapBiomas. Anos disponíveis: {anos_validos}. Pulando.")
            continue
            
        # URLs possíveis para o raster nacional
        urls = [
            f"https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_9/lclu/coverage/brasil_coverage_{ano}.tif",
            f"https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_8/lclu/coverage/brasil_coverage_{ano}.tif",
            f"https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_7/lclu/coverage/brasil_coverage_{ano}.tif",
            f"https://storage.googleapis.com/mapbiomas-public/collection_9/lclu/coverage/brasil_coverage_{ano}.tif",
            f"https://storage.googleapis.com/mapbiomas-public/COLECAO/9/ANUAL/BRASIL_COBERTURA/{ano}/coverage_{ano}.tif"
        ]
        
        # Nome temporário para o arquivo nacional
        nacional_dir = os.path.join(diretorio_base, "nacional")
        os.makedirs(nacional_dir, exist_ok=True)
        arquivo_nacional = os.path.join(nacional_dir, f"brasil_coverage_{ano}.tif")
        
        # Verifica se o arquivo nacional já existe
        arquivo_ja_existe = os.path.exists(arquivo_nacional)
        arquivo_baixado = False
        
        if arquivo_ja_existe:
            # Decide se utiliza o arquivo existente ou faz download novamente
            if ano in decisoes_arquivos["nacionais"]:
                # Usa decisão anterior
                usar_existente = not decisoes_arquivos["nacionais"][ano]
            elif substituir_arquivos is not None:
                # Usa parâmetro da função
                usar_existente = not substituir_arquivos
            else:
                # Pergunta ao usuário
                substituir = perguntar_substituir(arquivo_nacional)
                decisoes_arquivos["nacionais"][ano] = substituir
                usar_existente = not substituir
            
            if usar_existente:
                print(f"🔄 Utilizando arquivo nacional existente para {ano}: {os.path.basename(arquivo_nacional)}")
                logging.info(f"Utilizando arquivo nacional existente: {arquivo_nacional}")
                arquivos_nacionais.append(arquivo_nacional)
                arquivo_baixado = True
            else:
                print(f"🔄 Preparando para substituir arquivo nacional existente para {ano}")
                logging.info(f"Substituindo arquivo nacional existente: {arquivo_nacional}")
        
        # Se não temos arquivo ou decidimos substituir, fazemos o download
        if not arquivo_baixado:
            erros = []
            
            # Tenta baixar o arquivo de cada URL usando curl
            for url in urls:
                logging.info(f"Tentando baixar raster nacional para {ano} de: {url}")
                print(f"⬇️  Baixando raster nacional para {ano} de {url}...")
                
                try:
                    # Primeiro verifica se o arquivo existe com um HEAD request
                    check_cmd = ["curl", "-s", "-I", url]
                    resultado_check = subprocess.run(check_cmd, capture_output=True, text=True)
                    
                    if "200 OK" not in resultado_check.stdout and "HTTP/2 200" not in resultado_check.stdout:
                        erro = f"Arquivo não encontrado em {url} (status: não é 200 OK)"
                        erros.append(erro)
                        logging.warning(erro)
                        print(f"⚠️ {erro}")
                        continue
                        
                    # Baixa o arquivo usando curl com barra de progresso
                    cmd = ["curl", "-#", "-L", "-o", arquivo_nacional, url]
                    resultado = subprocess.run(cmd, check=True)
                    
                    if resultado.returncode == 0:
                        arquivos_nacionais.append(arquivo_nacional)
                        logging.info(f"Download concluído: {arquivo_nacional}")
                        print(f"✅ Raster nacional baixado: {os.path.basename(arquivo_nacional)}")
                        arquivo_baixado = True
                        break
                    else:
                        erro = f"Falha ao baixar de {url}: curl retornou código {resultado.returncode}"
                        erros.append(erro)
                        logging.warning(erro)
                        print(f"⚠️ {erro}")
                except subprocess.CalledProcessError as e:
                    erro = f"Falha ao baixar de {url}: {str(e)}"
                    erros.append(erro)
                    logging.warning(erro)
                    print(f"⚠️ {erro}")
                except Exception as e:
                    erro = f"Erro inesperado ao baixar de {url}: {str(e)}"
                    erros.append(erro)
                    logging.warning(erro)
                    print(f"⚠️ {erro}")
        
        if not arquivo_baixado:
            erro_msg = f"Erro ao baixar raster nacional para {ano}: Todas as tentativas falharam."
            logging.error(erro_msg)
            print(f"❌ {erro_msg}")
            print("Detalhes dos erros:")
            for i, erro in enumerate(erros, 1):
                print(f"  {i}. {erro}")
            continue
        
        # Cria diretório para o ano
        ano_dir = os.path.join(diretorio_base, str(ano))
        os.makedirs(ano_dir, exist_ok=True)
        
        # Recorta o raster nacional para cada município no shapefile
        for idx, feature in gdf.iterrows():
            # Mostra progresso a cada 1000 feições
            if idx % 1000 == 0:
                print(f"🔄 Processando feição {idx} de {len(gdf)}...")
                
            # Obtém o código do município
            if formato == "direto":
                cd_mun = str(feature[campo])
            else:  # formato == "extrair"
                cd_mun = extrair_cd_mun(feature[campo])
            
            if not cd_mun:
                logging.warning(f"Não foi possível extrair CD_MUN para a feição {idx}")
                continue
            
            # Nome do arquivo de saída para o município
            arquivo_municipio = os.path.join(ano_dir, f"{cd_mun}.tif")
            
            # Verifica se o arquivo municipal já existe
            arquivo_municipal_existe = os.path.exists(arquivo_municipio)
            
            # Chave composta para identificar município/ano
            chave_municipal = f"{cd_mun}_{ano}"
            
            if arquivo_municipal_existe:
                # Decide se utiliza o arquivo existente ou recorta novamente
                if chave_municipal in decisoes_arquivos["municipais"]:
                    # Usa decisão anterior
                    usar_existente = not decisoes_arquivos["municipais"][chave_municipal]
                elif substituir_arquivos is not None:
                    # Usa parâmetro da função
                    usar_existente = not substituir_arquivos
                else:
                    # Pergunta ao usuário
                    substituir = perguntar_substituir(arquivo_municipio)
                    decisoes_arquivos["municipais"][chave_municipal] = substituir
                    usar_existente = not substituir
                
                if usar_existente:
                    # Adiciona ao resultado e pula o recorte
                    if cd_mun not in resultados:
                        resultados[cd_mun] = []
                    resultados[cd_mun].append(arquivo_municipio)
                    
                    logging.info(f"Utilizando raster existente para {cd_mun}, ano {ano}: {arquivo_municipio}")
                    
                    # Mostra mensagem apenas para a primeira e última feição para não sobrecarregar o console
                    if idx == 0 or idx == len(gdf) - 1 or idx % 1000 == 0:
                        print(f"🔄 Utilizando recorte existente para município {cd_mun}, ano {ano} (feição {idx})")
                    continue
                else:
                    logging.info(f"Preparando para substituir raster existente para {cd_mun}, ano {ano}")
                    if idx == 0 or idx == len(gdf) - 1 or idx % 1000 == 0:
                        print(f"🔄 Preparando para substituir recorte existente para município {cd_mun}, ano {ano} (feição {idx})")
            
            try:
                # Prepara a geometria para recorte
                geometria = [feature.geometry.__geo_interface__]
                
                # Abre o raster nacional
                with rasterio.open(arquivo_nacional) as src:
                    # Recorta o raster pela geometria
                    out_image, out_transform = mask(src, geometria, crop=True, nodata=src.nodata)
                    
                    # Copia o metadata e atualiza a transformação
                    out_meta = src.meta.copy()
                    out_meta.update({
                        "driver": "GTiff",
                        "height": out_image.shape[1],
                        "width": out_image.shape[2],
                        "transform": out_transform
                    })
                    
                    # Salva o raster recortado
                    with rasterio.open(arquivo_municipio, "w", **out_meta) as dest:
                        dest.write(out_image)
                    
                    # Adiciona ao resultado
                    if cd_mun not in resultados:
                        resultados[cd_mun] = []
                    resultados[cd_mun].append(arquivo_municipio)
                    
                    logging.info(f"Raster recortado para {cd_mun}, ano {ano}: {arquivo_municipio}")
                    # Mostra mensagem apenas para a primeira e última feição para não sobrecarregar o console
                    if idx == 0 or idx == len(gdf) - 1 or idx % 1000 == 0:
                        print(f"✂️  Recorte para município {cd_mun}, ano {ano} concluído (feição {idx})")
            
            except Exception as e:
                logging.error(f"Erro ao recortar raster para município {cd_mun}, ano {ano}: {e}")
                print(f"❌ Erro ao recortar para {cd_mun}, ano {ano}: {e}")
    
    # Limpa diretórios vazios
    limpar_diretorios_vazios(diretorio_base)
    
    # Retorna resumo do processamento
    return resultados

async def main():
    """
    Função principal para execução do script.
    Processa os argumentos da linha de comando e inicia os downloads.
    """
    import argparse
    import os
    
    parser = argparse.ArgumentParser(
        description="Ferramenta para download e recorte de arquivos GeoTIFF do MapBiomas utilizando shapefile",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python -m src.downloader.downloader --shapefile shape/DF/APPS_1.shp --ano-inicio 2020 --ano-fim 2021
  python -m src.downloader.downloader --shapefile dados/municipios_brasil.shp --ano-inicio 2022 --ano-fim 2022
  python -m src.downloader.downloader --teste

O shapefile deve conter o campo CD_MUN com o código IBGE de 7 dígitos dos municípios,
ou o campo cod_imovel no formato "UF-CODIGO-XXXX" (ex: "DF-5300108-XXXX").

Valores padrão se não especificados:
  - Ano inicial: 1985
  - Ano final: 2023
  - Diretório de saída: ./downloads_mapbiomas/<ano>/<CD_MUN>.tif

Anos disponíveis:
  - Os dados do MapBiomas estão disponíveis apenas para os seguintes anos:
    1985, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2023
  - O programa processará automaticamente apenas os anos disponíveis.

Fonte de dados:
  - Collection 9 do MapBiomas
"""
    )
    
    grupo_dados = parser.add_argument_group('Opções de download')
    grupo_dados.add_argument("--shapefile", "-s", required=True, help="Caminho para shapefile com limites municipais")
    grupo_dados.add_argument("--ano-inicio", "-i", type=int, default=1985, help="Ano inicial (padrão: 1985)")
    grupo_dados.add_argument("--ano-fim", "-f", type=int, default=2023, help="Ano final (padrão: 2023)")
    grupo_dados.add_argument("--diretorio", "-d", default="downloads_mapbiomas", help="Diretório base para os arquivos baixados")
    grupo_dados.add_argument("--limite-feicoes", "-l", type=int, default=0, help="Limitar o número de feições processadas (0 = todas)")
    
    grupo_operacoes = parser.add_argument_group('Outras operações')
    grupo_operacoes.add_argument("--teste", "-t", action="store_true", help="Executa em modo de teste (sem download real)")
    grupo_operacoes.add_argument("--substituir", action="store_true", help="Substitui arquivos existentes sem perguntar")
    grupo_operacoes.add_argument("--manter", "--usar-existentes", action="store_true", help="Mantém arquivos existentes sem perguntar")
    
    args = parser.parse_args()
    
    # Verifica se foi especificado o shapefile (obrigatório)
    if not args.shapefile:
        print("❌ Erro: É necessário especificar um shapefile (--shapefile)")
        print("ℹ️  Use --help para ver todas as opções disponíveis")
        parser.print_help()
        return
    
    # Verifica conflito de opções
    if args.substituir and args.manter:
        print("❌ Erro: As opções --substituir e --manter não podem ser usadas juntas")
        return
    
    # Define o comportamento para arquivos existentes
    substituir_arquivos = None
    
    # Verifica a variável de ambiente V_MAPBIOMAS_REPLACE
    v_mapbiomas_replace = os.environ.get('V_MAPBIOMAS_REPLACE')
    if v_mapbiomas_replace is not None:
        try:
            v_mapbiomas_replace = int(v_mapbiomas_replace)
            # Se V_MAPBIOMAS_REPLACE=0, substituir arquivos
            # Se V_MAPBIOMAS_REPLACE=1, não substituir arquivos
            substituir_arquivos = v_mapbiomas_replace == 0
            print(f"ℹ️  Usando configuração do ambiente: {'substituir' if substituir_arquivos else 'manter'} arquivos existentes")
        except ValueError:
            print(f"⚠️  Valor inválido para V_MAPBIOMAS_REPLACE: {v_mapbiomas_replace}, usando padrão")
    
    # Parâmetros da linha de comando têm precedência sobre variáveis de ambiente
    if args.substituir:
        substituir_arquivos = True
    elif args.manter:
        substituir_arquivos = False
    
    # Processa por shapefile
    try:
        resultados = await baixar_e_recortar_por_shapefile(
            shapefile_path=args.shapefile,
            ano_inicio=args.ano_inicio,
            ano_fim=args.ano_fim,
            diretorio_base=args.diretorio,
            _teste=args.teste,
            limite_feicoes=args.limite_feicoes,
            substituir_arquivos=substituir_arquivos,
            utilizar_existentes=args.manter
        )
        
        # Imprime resumo
        if resultados:
            print(f"\n📊 Resumo do processamento com shapefile:")
            print(f"   ✅ Municípios processados: {len(resultados)}")
            for cd_mun, arquivos in resultados.items():
                print(f"     - {cd_mun}: {len(arquivos)} anos processados")
        else:
            print("\n❌ Não foram gerados resultados. Verifique os erros acima.")
    except Exception as e:
        logging.error(f"Erro ao processar shapefile {args.shapefile}: {e}")
        print(f"❌ Erro: {e}")
    finally:
        # Limpa diretórios vazios mesmo em caso de erro
        if args.diretorio:
            limpar_diretorios_vazios(args.diretorio)

if __name__ == "__main__":
    asyncio.run(main()) 