import re


def correct_ocr_text(text):
    """Corrige erros comuns do OCR, como confusão entre números e letras."""
    # Correção de alguns erros comuns
    text = text.replace('0', 'O')
    text = text.replace('1', 'I')
    return text


def validate_plate_format(text):
    """Valida se o texto extraído segue um formato de placa reconhecível."""
    pattern = r'[A-Z]{3}-\d{4}'
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return None


