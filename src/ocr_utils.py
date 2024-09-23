import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import cv2


def perform_ocr(img):
    # Verificar se a imagem está em escala de cinza, caso contrário, converter
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # Converter para 8 bits se a imagem não estiver nesse formato
    if gray.dtype != 'uint8':
        gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')

    # Aplicar threshold binário para melhorar a legibilidade do OCR
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Realizar o OCR na imagem processada
    text = pytesseract.image_to_string(thresh, config='--psm 8')  # '--psm 8' assume que estamos lendo um único caractere ou bloco de texto

    return text
