import os
import cv2
from argparse import ArgumentParser, RawTextHelpFormatter
from src import config, image_utils, ocr_utils
from src import evaluation_utils  # Import da função de avaliação WER
import pandas as pd  # Importar pandas para salvar os resultados em planilhas


def __get_args():
    parser = ArgumentParser(prog="ProjetoPdI", description="", formatter_class=RawTextHelpFormatter)
    parser.add_argument("-in", "--input", dest="input_dir", default=config.RAW_DIR, help="Input dir path")
    parser.add_argument("-out", "--output", dest="output_dir", default=config.OUTPUT_DIR, help="Output dir")
    return parser.parse_args()


def save_results_to_excel(results, output_path):
    # Criar uma lista de dicionários com os resultados
    data = []
    for result in results:
        name, recognized_text, wer_score = result
        if wer_score is None:
            wer_value = "N/A"
            quality = "Ruim"
        else:
            wer_value = wer_score
            quality = "Bom" if wer_score < 0.5 else "Ruim"

        data.append({"Pipeline": name, "Texto Reconhecido": recognized_text, "WER": wer_value, "Qualidade": quality})

    # Criar um DataFrame do pandas a partir dos resultados
    df = pd.DataFrame(data)

    # Salvar como arquivo CSV
    df.to_csv(output_path.replace('.xlsx', '.csv'), index=False)
    print(f"Resultados salvos em: {output_path.replace('.xlsx', '.csv')}")


def process_image(img):
    print("Iniciando o processamento de imagem...")

    # Passo 1: Aplicar pré-processamento e segmentações diferentes
    preprocessed_img = image_utils.preprocessing(img)

    # Testar diferentes filtros de suavização
    bilateral_img = image_utils.bilateral_filter(preprocessed_img)
    equalized_img = image_utils.histogram_equalization(preprocessed_img)

    # Testar técnicas de binarização
    niblack_img = image_utils.binarize_niblack(preprocessed_img)
    otsu_img = image_utils.binarize_otsu(preprocessed_img)

    # Aplicar diferentes segmentações
    segmented_img = image_utils.segmentation(preprocessed_img)
    edges_img = image_utils.detect_edges(segmented_img)
    region_segmented_img = image_utils.region_based_segmentation(img)
    kmeans_img = image_utils.kmeans_segmentation(preprocessed_img)
    components_img = image_utils.connected_components_segmentation(preprocessed_img)

    print("Processamento de imagem concluído.")
    return {
        "segmented": segmented_img,
        "edges": edges_img,
        "region_segmented": region_segmented_img,
        "bilateral": bilateral_img,
        "equalized": equalized_img,
        "niblack": niblack_img,
        "otsu": otsu_img,  # Adicionando Otsu à análise
        "kmeans": kmeans_img,
        "components": components_img
    }


def evaluate_ocr_with_pipelines(img, true_text):
    pipelines = {
        "Pipeline 1 (Otsu + Watershed)": {
            "preprocessing": image_utils.preprocessing,
            "binarization": image_utils.binarize_otsu,
            "segmentation": image_utils.region_based_segmentation
        },
        "Pipeline 2 (Niblack + K-Means)": {
            "preprocessing": image_utils.preprocessing,
            "binarization": image_utils.binarize_niblack,
            "segmentation": image_utils.kmeans_segmentation
        },
        "Pipeline 3 (Otsu + Componentes Conexos)": {
            "preprocessing": image_utils.preprocessing,
            "binarization": image_utils.binarize_otsu,
            "segmentation": image_utils.connected_components_segmentation
        },
        "Pipeline 4 (Adaptive Threshold + Contours)": {
            "preprocessing": image_utils.preprocessing,
            "binarization": image_utils.adaptive_threshold,
            "segmentation": image_utils.simple_contour_segmentation
        },
        "Pipeline 5 (CLAHE + Contours)": {
            "preprocessing": image_utils.apply_clahe,
            "binarization": image_utils.binarize_otsu,
            "segmentation": image_utils.simple_contour_segmentation
        }
    }

    results = []

    for name, steps in pipelines.items():
        print(f"Avaliando {name}...")

        # Aplicar as etapas do pipeline
        preprocessed_img = steps["preprocessing"](img)
        binarized_img = steps["binarization"](preprocessed_img)
        segmented_img = steps["segmentation"](binarized_img)

        # Recortar caracteres
        cropped_chars = image_utils.crop_characters(segmented_img)

        # Limitar o número de caracteres recortados (por exemplo, no máximo 50)
        if len(cropped_chars) > 50:
            print(f"Número excessivo de caracteres recortados: {len(cropped_chars)}. Limitando a 50.")
            cropped_chars = cropped_chars[:50]

        # Reconhecer os caracteres
        recognized_text = ''.join([ocr_utils.perform_ocr(cropped) for cropped in cropped_chars])

        # Verificar se o texto reconhecido ou o verdadeiro está vazio
        if not recognized_text.strip() or not true_text.strip():
            print(f"Texto verdadeiro ou reconhecido está vazio. WER não será calculado para {name}.")
            wer_score = None
        else:
            # Avaliar WER apenas se os textos não estiverem vazios
            wer_score = evaluation_utils.calculate_wer(true_text, recognized_text)

        results.append((name, recognized_text, wer_score))

    return results


def display_results(results):
    print("\nResultados:")
    print("{:<30} | {:<30} | {:<10} | {:<10}".format("Pipeline", "Texto Reconhecido", "WER", "Qualidade"))
    print("-" * 80)

    for result in results:
        name, recognized_text, wer_score = result
        if wer_score is None:
            quality = "Ruim"
            print(f"{name:<30} | {recognized_text:<30} | {'N/A':<10} | {quality:<10}")
        else:
            quality = "Bom" if wer_score < 0.5 else "Ruim"
            print(f"{name:<30} | {recognized_text:<30} | {wer_score:<10.2f} | {quality:<10}")


def main():
    args = __get_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Texto verdadeiro (deve ser ajustado conforme as imagens)
    true_texts = {
        "1.png": "12345",
        "2.png": "67890",
        "3.png": "AB1234",
        "4.png": "XYZ789",
        "5.png": "98765",
        "6.png": "POI567",
        # Adicione mais textos verdadeiros conforme as imagens
    }

    all_results = []

    for filename in os.listdir(input_dir):
        print(f"Processando imagem: {filename}")
        image_path = os.path.join(input_dir, filename)

        img = cv2.imread(image_path)

        if img is None:
            print(f"Falha ao carregar a imagem {filename}")
            continue

        # Processar e salvar as imagens
        processed_images = process_image(img)

        for key, processed_img in processed_images.items():
            output_path = os.path.join(output_dir, f"{key}_{filename}")
            cv2.imwrite(output_path, processed_img)
            print(f"Imagem {key} salva em: {output_path}")

        # Obter o texto verdadeiro da imagem
        true_text = true_texts.get(filename, "")

        # Avaliar OCR com diferentes pipelines e calcular WER
        results = evaluate_ocr_with_pipelines(img, true_text)
        all_results.extend(results)

        # Exibir resultados em forma de tabela
        display_results(results)

    # Salvar os resultados em uma planilha Excel
    save_results_to_excel(all_results, os.path.join(output_dir, "resultados_ocr.xlsx"))


if __name__ == '__main__':
    main()
