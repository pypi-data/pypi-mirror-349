# src/tests/test_downloader.py
# Author: Ricardo Malnati

"""
Este módulo contém os testes unitários e de ponta a ponta para o Downloader de MapBiomas.
"""

import os
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.downloader.downloader import verificar_cd_mun, extrair_cd_mun


class TestDownloader:
    """
    Classe de testes para o Downloader.
    """

    def test_extrair_cd_mun(self):
        """
        Testa a função que extrai o código do município de uma string.
        """
        # Testes com códigos válidos
        assert extrair_cd_mun("DF-5300108-FE82A26B95AB481A9FB79E3AD8736D3E") == "5300108"
        assert extrair_cd_mun("SE-2802106-CF30DCBC32584457B43D79C7FF8F0EE2") == "2802106"
        
        # Testes com formatos inválidos
        assert extrair_cd_mun("") == ""
        assert extrair_cd_mun("FORMATO_INVALIDO") == ""
        assert extrair_cd_mun("DF-530010-INCOMPLETO") == ""
        assert extrair_cd_mun("DF-ABCDEFG-INVALIDO") == ""
    
    @patch('geopandas.read_file')
    def test_verificar_cd_mun(self, mock_read_file):
        """
        Testa a função que verifica a existência do campo CD_MUN no shapefile.
        """
        # Mock para shapefile com CD_MUN presente
        mock_gdf_com_cd_mun = MagicMock()
        mock_gdf_com_cd_mun.columns = ["CD_MUN", "geometry", "area"]
        mock_gdf_com_cd_mun.empty = False
        
        # Mock para shapefile sem CD_MUN, mas com formato cod_imovel
        mock_gdf_com_cod_imovel = MagicMock()
        mock_gdf_com_cod_imovel.columns = ["cod_imovel", "geometry", "area"]
        mock_gdf_com_cod_imovel.empty = False
        mock_gdf_com_cod_imovel["cod_imovel"].iloc = MagicMock()
        mock_gdf_com_cod_imovel["cod_imovel"].iloc[0] = "DF-5300108-XYZ123"
        
        # Mock para shapefile sem CD_MUN e sem alternativa
        mock_gdf_sem_alternativa = MagicMock()
        mock_gdf_sem_alternativa.columns = ["outro_campo", "geometry", "area"]
        mock_gdf_sem_alternativa.empty = False
        
        # Configura o comportamento do mock para o teste 1
        mock_read_file.return_value = mock_gdf_com_cd_mun
        
        # Testa shapefile com CD_MUN presente
        resultado1 = verificar_cd_mun("mock_path1.shp")
        assert resultado1 == {"campo": "CD_MUN", "formato": "direto"}
        
        # Configura o comportamento do mock para o teste 2
        mock_read_file.return_value = mock_gdf_com_cod_imovel
        
        # Testa shapefile com cod_imovel - usando o modo de teste
        resultado2 = verificar_cd_mun("mock_path2.shp", _teste=True)
        assert resultado2 == {"campo": "cod_imovel", "formato": "extrair"}
        
        # Configura o comportamento do mock para o teste 3
        mock_read_file.return_value = mock_gdf_sem_alternativa
        
        # Testa shapefile sem CD_MUN e sem alternativa
        with pytest.raises(ValueError, match="não contém o campo CD_MUN ou equivalente"):
            verificar_cd_mun("mock_path3.shp")
        
        # Verifica se o mock foi chamado corretamente
        assert mock_read_file.call_count == 3

    @patch('os.makedirs')
    def test_baixar_e_recortar_por_shapefile(self, mock_makedirs):
        """
        Testa o fluxo de baixar e recortar por shapefile.
        """
        from src.downloader.downloader import baixar_e_recortar_por_shapefile
        import asyncio
        
        # Cria um GeoDataFrame simulado com uma geometria
        mock_feature = MagicMock()
        mock_feature.geometry = MagicMock()
        mock_feature.geometry.__geo_interface__ = {"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}
        mock_feature.__getitem__ = MagicMock(return_value="5300108")  # Simula o acesso a CD_MUN
        
        mock_gdf = MagicMock()
        mock_gdf.iterrows.return_value = [(0, mock_feature)]
        mock_gdf.__len__.return_value = 1
        
        # Mock da função verificar_cd_mun e geopandas.read_file
        with patch('src.downloader.downloader.verificar_cd_mun') as mock_verificar:
            mock_verificar.return_value = {"campo": "CD_MUN", "formato": "direto"}
            
            with patch('geopandas.read_file') as mock_read_file:
                mock_read_file.return_value = mock_gdf
                
                # Executa a função de teste em modo de teste
                resultados = asyncio.run(baixar_e_recortar_por_shapefile(
                    shapefile_path="teste.shp",
                    ano_inicio=2020,
                    ano_fim=2020,
                    diretorio_base="teste_downloads",
                    _teste=True
                ))
                
                # Verificações
                assert isinstance(resultados, dict)
                assert "5300108" in resultados
                assert len(resultados["5300108"]) == 1  # Um ano processado
                
                # Verifica se os diretórios foram criados
                assert mock_makedirs.call_count >= 3  # diretório base, pasta nacional, pasta do ano 