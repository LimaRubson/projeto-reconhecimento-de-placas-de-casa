import cv2
import numpy as np


def adaptive_threshold(img):
    print("Aplicando Adaptive Thresholding...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)
    print("Adaptive Thresholding aplicado.")
    return adaptive_thresh


def simple_contour_segmentation(img):
    print("Segmentando a imagem usando Contornos...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    _, binary_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Encontrar contornos
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Desenhar contornos
    segmented_img = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 1)

    print("Segmentação por contornos concluída.")
    return segmented_img


def apply_clahe(img):
    print("Aplicando CLAHE para melhorar o contraste...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced_img = clahe.apply(gray)
    print("CLAHE aplicado.")
    return enhanced_img


def preprocessing(img):
    print("Aplicando pré-processamento (conversão para tons de cinza)...")
    if len(img.shape) == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # Normaliza a imagem
    normalized_img = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    print("Pré-processamento concluído.")
    return normalized_img


#Pré-processamento avançado
def crop_characters(img):
    print("Recortando caracteres individualmente...")
    # Verificar se a imagem está em escala de cinza, caso contrário, converter
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

    # Converter a imagem para o formato de 8 bits se necessário
    if gray.dtype != np.uint8:
        gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Aplicar binarização Otsu
    _, binary_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Encontrar contornos para isolar os números
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cropped_images = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Recortar o número e armazená-lo
        cropped = img[y:y + h, x:x + w]
        cropped_images.append(cropped)

    print(f"{len(cropped_images)} caracteres recortados.")
    return cropped_images


def blur_image(img):
    print("Aplicando desfoque Gaussian para reduzir ruído...")
    blurred_img = cv2.GaussianBlur(img, (5, 5), 0)
    print("Desfoque aplicado.")
    return blurred_img


def bilateral_filter(img):
    print("Aplicando filtro bilateral...")
    filtered_img = cv2.bilateralFilter(img, 9, 75, 75)
    print("Filtro bilateral aplicado.")
    return filtered_img


def histogram_equalization(img):
    print("Aplicando equalização de histograma...")
    if len(img.shape) == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    equalized_img = cv2.equalizeHist(gray)
    print("Equalização de histograma concluída.")
    return equalized_img


def binarize_otsu(img):
    print("Aplicando binarização Otsu...")
    _, binary_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print("Binarização concluída.")
    return binary_img


def binarize_niblack(img):
    print("Aplicando binarização Niblack...")
    if len(img.shape) == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    mean, std_dev = cv2.meanStdDev(gray)
    binary_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY_INV, 11, 2)
    print("Binarização Niblack concluída.")
    return binary_img


def segmentation(img):
    print("Segmentando a imagem...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    _, segmented_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print("Segmentação concluída.")
    return segmented_img


def detect_edges(img):
    print("Detectando bordas na imagem...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    edges = cv2.Canny(gray, 100, 200)
    print("Detecção de bordas concluída.")
    return edges


def region_based_segmentation(img):
    print("Segmentando a imagem por regiões usando Watershed...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 0] = 0

    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) if len(img.shape) == 2 else img
    markers = cv2.watershed(img_color, markers)
    img_color[markers == -1] = [255, 0, 0]

    print("Segmentação por regiões concluída.")
    return img_color


def kmeans_segmentation(img, k=2):
    print("Aplicando segmentação K-Means...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    img_flat = np.float32(gray.reshape((-1, 1)))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(img_flat, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    segmented_img = centers[labels.flatten()].reshape(img.shape)
    print("Segmentação K-Means concluída.")
    return np.uint8(segmented_img)


def connected_components_segmentation(img):
    print("Aplicando segmentação por componentes conexos...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    _, binary_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    num_labels, labels, _, _ = cv2.connectedComponentsWithStats(binary_img, connectivity=8)
    print("Segmentação por componentes conexos concluída.")
    return labels
