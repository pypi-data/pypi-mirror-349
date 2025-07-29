# MapBiomas Downloader

Ferramenta para download de arquivos GeoTIFF do MapBiomas para municípios ou estados brasileiros.

## Instalação

### Requisitos

- Python 3.12+
- Poetry

### Configuração do ambiente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/mapbiomas-downloader.git
cd mapbiomas-downloader
```

2. Configure o ambiente Python com pyenv (recomendado):
```bash
pyenv install 3.12
pyenv local 3.12
```

3. Instale as dependências com Poetry:
```bash
poetry install
```

## Uso do downloader

O downloader pode ser executado diretamente usando o script shell fornecido:

### Baixar dados para um município específico

```bash
./downloader.sh --municipio 3550308 --ano-inicio 2020 --ano-fim 2021
```

### Baixar dados para um estado completo

```bash
./downloader.sh --estado SP --ano-inicio 2020 --ano-fim 2021
```

### Opções disponíveis

- `--municipio` ou `-m`: Código IBGE do município (7 dígitos)
- `--estado` ou `-e`: Sigla do estado (UF)
- `--ano-inicio` ou `-i`: Ano inicial para download (padrão: 1985)
- `--ano-fim` ou `-f`: Ano final para download (padrão: 2023)
- `--diretorio` ou `-d`: Diretório base para salvar os arquivos (padrão: downloads_mapbiomas)

## Executando os Testes

Este projeto utiliza pytest para a execução de testes automatizados. Os testes estão localizados no diretório `src/tests`.

### Executar todos os testes

```bash
poetry run pytest
```

### Executar testes com relatório de cobertura

```bash
poetry run pytest --cov=src
```

### Executar testes específicos

```bash
poetry run pytest src/tests/test_downloader.py::TestDownloader::test_is_valid_state
```

### Analisando os Resultados dos Testes

Os testes geram relatórios que ajudam a verificar se todas as funcionalidades estão operando corretamente:

- **Verificação de funcionalidades**: Os testes unitários verificam se cada função da biblioteca funciona isoladamente.
- **Teste E2E (end-to-end)**: Simulam o fluxo completo de download de arquivos do MapBiomas.
- **Cobertura de código**: O relatório de cobertura indica quais partes do código estão sendo testadas adequadamente.

## Uso da Biblioteca

```python
from src.downloader import Downloader

# Verificar se um estado é válido
Downloader.is_valid_state("SP")  # True

# Obter o código IBGE de um estado
codigo_sp = Downloader.get_state_code("SP")  # "35"

# Obter as cidades de um estado
cidades_sp = Downloader.get_cities_by_state("SP")

# Validar código de cidade
Downloader.is_valid_city_code("3550308")  # True - São Paulo capital
```

## Contribuição

1. Sempre crie e ative um ambiente virtual antes de trabalhar no projeto
2. Execute os testes antes de enviar suas alterações
3. Mantenha a documentação atualizada

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
