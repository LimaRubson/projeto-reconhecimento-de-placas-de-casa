# Projeto de Reconhecimento de Placas de Casas
Este projeto tem como objetivo desenvolver um sistema de reconhecimento de placas de casas utilizando técnicas de processamento de imagens e OCR (Reconhecimento Óptico de Caracteres). O sistema é capaz de processar imagens contendo números de placas e, através de segmentação, detecção de bordas e outras técnicas, identificar os números presentes.

## Estrutura do Projeto
reconhecimento-placas/
│
├── src/
│   ├── __init__.py                    # Arquivo de inicialização do pacote src
│   ├── image_utils.py                 # Funções de pré-processamento, segmentação e pós-processamento
│   ├── ocr_utils.py                   # Funções relacionadas ao OCR
│   ├── post_processing.py             # Funções de pós-processamento (correção, validação)
│   ├── config.py                      # Configurações e parâmetros globais
│   ├── tests/
│       ├── test_image_utils.py        # Testes unitários para image_utils
│       ├── test_ocr_utils.py          # Testes unitários para ocr_utils
│       ├── test_post_processing.py    # Testes para pós-processamento
│
├── data/
│   ├── raw/                           # Imagens de entrada para testes
│   ├── processed/                     # Imagens processadas
│   ├── output/                        # Resultados finais
│
├── docs/
│   ├── README.md                      # Documentação do projeto
│   ├── requirements.txt               # Dependências e pacotes Python
│
├── main.py                            # Script principal para execução
└── setup.py                           # Script de setup e instalação

## Funcionalidades
 Pré-processamento de Imagens: Aplicação de filtros de suavização e técnicas de binarização para preparação da imagem para segmentação.
 Segmentação de Imagens: Algoritmos de segmentação tradicional (thresholding) e por regiões (Watershed).
 Detecção de Bordas: Utilização do método de Canny para realçar os contornos dos números.
 OCR: Reconhecimento dos números após o processamento da imagem.
 Pós-processamento: Validação e correção dos resultados do OCR.

## Requisitos
Para rodar o projeto, é necessário instalar as dependências descritas no arquivo requirements.txt. Para isso, execute o seguinte comando:

pip install -r docs/requirements.txt

## Principais Dependências
OpenCV: Biblioteca principal para manipulação de imagens.
NumPy: Utilizado para operações matemáticas e manipulação de arrays.
Tesseract-OCR: Motor de OCR para o reconhecimento de caracteres.

## Como Usar
Coloque as imagens das placas que você deseja processar no diretório data/raw.
Execute o arquivo main.py para processar as imagens:

python main.py

## As imagens processadas serão salvas no diretório data/output.
Exemplo de Execução

python main.py --input data/raw/ --output data/output/


## Argumentos Opcionais
--input: Diretório contendo as imagens a serem processadas (padrão: data/raw).
--output: Diretório onde serão salvas as imagens processadas (padrão: data/output).

## Testes
O projeto inclui testes unitários para as principais funções implementadas. Para executar os testes, utilize o seguinte comando:

pytest src/tests/

Os testes cobrem as funções de pré-processamento, segmentação, OCR e pós-processamento.

## Estrutura de Código
image_utils.py
Contém funções essenciais para o processamento das imagens:

segmentação: Converte a imagem para escala de cinza e aplica um limiar adaptativo.
detect_edges: Utiliza o método Canny para detectar as bordas dos números.
region_based_segmentation: Implementa a técnica de Watershed para segmentação baseada em regiões.
isolate_number: Isola os números da imagem para facilitar a etapa de OCR.
ocr_utils.py
Contém as funções responsáveis pelo reconhecimento óptico dos números, utilizando o Tesseract.

post_processing.py
Realiza correções nos resultados obtidos pelo OCR e verifica se os números identificados estão dentro de um padrão esperado.

## Contribuição
Contribuições são bem-vindas! Se você encontrar algum bug ou tiver sugestões de melhorias, por favor, abra uma issue ou envie um pull request.

## Autor
    Rubson Hebrain de Lima Freire

## Referências
Documentação do OpenCV: https://docs.opencv.org/
Tesseract OCR: https://github.com/tesseract-ocr/tesseract
