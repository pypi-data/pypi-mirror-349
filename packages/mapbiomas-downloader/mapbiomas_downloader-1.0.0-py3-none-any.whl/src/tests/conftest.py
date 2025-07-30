"""
Configurações e fixtures para os testes do MapBiomas Downloader.
"""
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_state_info():
    """Fixture que retorna informações de estados para os testes."""
    return {
        "SP": {"codigo": "35", "nome": "São Paulo"},
        "RJ": {"codigo": "33", "nome": "Rio de Janeiro"},
        "MG": {"codigo": "31", "nome": "Minas Gerais"},
    }


@pytest.fixture
def mock_city_info():
    """Fixture que retorna informações de cidades para os testes."""
    return {
        "3550308": {
            "ibge": "3550308",
            "nome": "São Paulo",
            "uf": "SP"
        },
        "3304557": {
            "ibge": "3304557",
            "nome": "Rio de Janeiro",
            "uf": "RJ"
        },
        "3106200": {
            "ibge": "3106200",
            "nome": "Belo Horizonte",
            "uf": "MG"
        }
    }


@pytest.fixture
def mock_playwright():
    """Mock para o playwright usado nos testes E2E."""
    with patch('playwright.async_api.async_playwright') as mock:
        # Configura a cadeia de mocks
        mock_playwright_instance = MagicMock()
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()
        mock_download = MagicMock()
        
        # Conecta os mocks
        mock.return_value.__aenter__.return_value = mock_playwright_instance
        mock_playwright_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_page.wait_for_event.return_value = mock_download
        
        yield mock 