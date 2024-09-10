import os

# Definir diretórios principais
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')

# Parâmetros para segmentação
SEGMENTATION_METHOD = 'watershed'  # Pode ser 'watershed' ou 'kmeans'

# Parâmetros para OCR
OCR_LANG = 'eng'  # Idioma para Tesseract OCR

# Outras configurações
DEBUG_MODE = True  # Exibe informações de debug
