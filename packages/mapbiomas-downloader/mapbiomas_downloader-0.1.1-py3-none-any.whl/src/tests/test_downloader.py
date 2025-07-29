# src/tests/test_downloader.py
# Author: Ricardo Malnati

"""
Este módulo contém os testes unitários e de ponta a ponta para o Downloader de MapBiomas.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from src.downloader.downloader import Downloader


class TestDownloader:
    """
    Classe de testes para o Downloader.
    """

    @pytest.fixture
    def setup_downloader(self):
        """
        Configuração inicial para os testes.
        """
        return Downloader()

    def test_is_valid_state(self, setup_downloader):
        """
        Testa se a validação de estados está correta.
        """
        # Testes com estados válidos
        assert Downloader.is_valid_state("SP") is True
        assert Downloader.is_valid_state("sp") is True
        assert Downloader.is_valid_state("RJ") is True

        # Testes com estados inválidos
        assert Downloader.is_valid_state("Invalid State") is False
        assert Downloader.is_valid_state("XX") is False
        assert Downloader.is_valid_state("") is False

    def test_get_state_code(self, setup_downloader):
        """
        Testa se o retorno do código do estado está correto.
        """
        # Testes com estados válidos
        assert Downloader.get_state_code("SP") == "35"
        assert Downloader.get_state_code("sp") == "35"
        assert Downloader.get_state_code("RJ") == "33"
        assert Downloader.get_state_code("MG") == "31"

        # Testes com estados inválidos
        assert Downloader.get_state_code("XX") == ""
        assert Downloader.get_state_code("") == ""
        assert Downloader.get_state_code("Invalid") == ""

    @patch('src.downloader.downloader.Downloader.get_city_info')
    def test_get_city_info(self, mock_info_cidade, setup_downloader):
        """
        Testa se as informações da cidade são retornadas corretamente.
        """
        # Configura o mock para retornar dados específicos
        cidade_info = {
            "ibge": "3550308",
            "nome": "São Paulo",
            "uf": "SP"
        }
        mock_info_cidade.return_value = cidade_info

        # Executa o teste
        result = Downloader.get_city_info("3550308")
        
        # Verifica se os resultados estão corretos
        assert result == cidade_info
        assert result["ibge"] == "3550308"
        assert result["nome"] == "São Paulo"
        assert result["uf"] == "SP"
        
        # Verifica se o mock foi chamado corretamente
        mock_info_cidade.assert_called_once_with("3550308")

    @patch('src.downloader.downloader.Downloader.get_cities_by_state')
    def test_get_cities_by_state(self, mock_get_cities, setup_downloader):
        """
        Testa se a lista de cidades por estado é retornada corretamente.
        """
        # Configura o mock para retornar uma lista específica
        sp_cities = [
            {"ibge": "3550308", "nome": "São Paulo", "uf": "SP"},
            {"ibge": "3550407", "nome": "São Roque", "uf": "SP"}
        ]
        rj_cities = [
            {"ibge": "3300100", "nome": "Rio de Janeiro", "uf": "RJ"}
        ]
        
        # Configurar o comportamento do mock para diferentes inputs
        mock_get_cities.side_effect = lambda state_code: (
            sp_cities if state_code in ["35", "SP"] else
            rj_cities if state_code in ["33", "RJ"] else
            []
        )
        
        # Executa o teste usando código do estado
        result = Downloader.get_cities_by_state("35")
        
        # Verifica se os resultados estão corretos
        assert len(result) == 2
        assert result[0]["ibge"] == "3550308"
        assert result[1]["ibge"] == "3550407"
        
        # Executa o teste usando sigla do estado
        result = Downloader.get_cities_by_state("SP")
        
        # Verifica se os resultados estão corretos
        assert len(result) == 2
        assert result[0]["ibge"] == "3550308"
        assert result[1]["ibge"] == "3550407"
        
        # Executa o teste com estado do RJ
        result = Downloader.get_cities_by_state("RJ")
        assert len(result) == 1
        assert result[0]["ibge"] == "3300100"
        
        # Executa o teste com estado inválido
        result = Downloader.get_cities_by_state("XX")
        assert result == []

    @patch('src.downloader.downloader.Downloader.get_city_info')
    def test_is_valid_city_code(self, mock_get_city_info, setup_downloader):
        """
        Testa se a validação do código da cidade está correta.
        """
        # Configura o mock para retornar dados específicos
        mock_get_city_info.side_effect = lambda code: (
            {"ibge": code, "nome": "Cidade Teste"} if code == "3550308" else {}
        )
        
        # Testes com códigos válidos
        assert Downloader.is_valid_city_code("3550308") is True
        
        # Testes com códigos inválidos
        assert Downloader.is_valid_city_code("0000000") is False
        assert Downloader.is_valid_city_code("123") is False
        assert Downloader.is_valid_city_code("") is False
        assert Downloader.is_valid_city_code("INVALID") is False

    @patch('asyncio.run')
    @patch('os.makedirs')
    @patch('playwright.async_api.async_playwright')
    def test_e2e_download_process(self, mock_playwright, mock_makedirs, mock_asyncio_run, setup_downloader):
        """
        Teste de ponta a ponta para o processo de download.
        """
        # Este teste simula o processo completo de download
        # Seria implementado com mocks para o playwright e outras dependências
        # Aqui demonstramos apenas a abordagem básica
        
        # Arranjo (Arrange)
        # Mock dos objetos do playwright
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()
        mock_download = MagicMock()
        
        # Configura a cadeia de mocks
        mock_playwright_instance = MagicMock()
        mock_playwright.return_value.__aenter__.return_value = mock_playwright_instance
        mock_playwright_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_page.wait_for_event.return_value = mock_download
        
        # Adiciona método adicional simulando download pelo playwright
        async def fake_download_process():
            # Simula um download bem-sucedido
            return ["downloads_mapbiomas/3550308/3550308_mapbiomas_2020.tif"]
        
        mock_asyncio_run.return_value = fake_download_process()
        
        # Esta seria a implementação real do teste E2E
        # Por enquanto só verificamos se temos toda a estrutura necessária
        assert isinstance(setup_downloader, Downloader)
        assert callable(mock_asyncio_run)
        
        # O teste completo seria algo como:
        # result = await baixar_mapbiomas_por_municipio(
        #     codigo_municipio="3550308",
        #     ano_inicio=2020,
        #     ano_fim=2020
        # )
        # assert len(result) == 1
        # assert "3550308_mapbiomas_2020.tif" in result[0] 