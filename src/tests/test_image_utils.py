import unittest
import cv2
import os
from src import image_utils, config

class TestImageUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.img_path = os.path.join(config.RAW_DIR, 'placa.jpg')
        cls.img = cv2.imread(cls.img_path)

    def test_preprocess_image(self):
        """Teste para a função de pré-processamento."""
        preprocessed_img = image_utils.preprocess_image(self.img)
        self.assertIsNotNone(preprocessed_img, "A imagem pré-processada não deveria ser None")
        self.assertEqual(preprocessed_img.shape, self.img.shape[:2], "A imagem deve ser convertida para tons de cinza")

    def test_watershed_segmentation(self):
        """Teste para segmentação Watershed."""
        segmented_img = image_utils.segment_image(self.img, method="watershed")
        self.assertIsNotNone(segmented_img, "A imagem segmentada não deveria ser None")

    def test_kmeans_segmentation(self):
        """Teste para segmentação K-Means."""
        segmented_img = image_utils.segment_image(self.img, method="kmeans")
        self.assertIsNotNone(segmented_img, "A imagem segmentada não deveria ser None")

if __name__ == '__main__':
    unittest.main()
