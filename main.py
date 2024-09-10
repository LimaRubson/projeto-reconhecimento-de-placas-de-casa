import os
import cv2
from argparse import ArgumentParser, RawTextHelpFormatter
from src import config, image_utils, ocr_utils


def __get_args():
    parser = ArgumentParser(prog="ProjetoPdI", description="", formatter_class=RawTextHelpFormatter)
    parser.add_argument("-in", "--input", dest="input_dir", default=config.RAW_DIR, help="Input dir path")
    parser.add_argument("-out", "--output", dest="output_dir", default=config.OUTPUT_DIR, help="Output dir")
    return parser.parse_args()


def process_image(img):
    print("Iniciando o processamento de imagem...")

    # Passo 1: Aplicar pré-processamento e segmentações diferentes
    preprocessed_img = image_utils.preprocessing(img)
    bilateral_img = image_utils.bilateral_filter(preprocessed_img)
    equalized_img = image_utils.histogram_equalization(preprocessed_img)
    niblack_img = image_utils.binarize_niblack(preprocessed_img)

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
        "kmeans": kmeans_img,
        "components": components_img
    }


def main():
    args = __get_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        print(f"Processando imagem: {filename}")
        image_path = os.path.join(input_dir, filename)

        img = cv2.imread(image_path)

        if img is None:
            print(f"Falha ao carregar a imagem {filename}")
            continue

        processed_images = process_image(img)

        for key, processed_img in processed_images.items():
            output_path = os.path.join(output_dir, f"{key}_{filename}")
            cv2.imwrite(output_path, processed_img)
            print(f"Imagem {key} salva em: {output_path}")

        # Aplicar OCR e salvar o resultado
        ocr_text = ocr_utils.perform_ocr(processed_images["segmented"])
        print(f"Texto reconhecido: {ocr_text}")


if __name__ == '__main__':
    main()
