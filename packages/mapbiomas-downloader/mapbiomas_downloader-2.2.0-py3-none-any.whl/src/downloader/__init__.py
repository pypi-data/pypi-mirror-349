"""
MapBiomas Downloader - Módulo para download e recorte de dados geoespaciais do MapBiomas usando shapefile.

Autor: Ricardo Malnati
"""

from .downloader import verificar_cd_mun, extrair_cd_mun, baixar_e_recortar_por_shapefile

# Função de entrada para ser chamada por scripts externos
def run_main():
    """
    Ponto de entrada para chamar a função main do downloader.
    Evita problemas de importação circular.
    """
    import asyncio
    from .downloader import main
    asyncio.run(main())

__all__ = ["verificar_cd_mun", "extrair_cd_mun", "baixar_e_recortar_por_shapefile", "run_main"] 