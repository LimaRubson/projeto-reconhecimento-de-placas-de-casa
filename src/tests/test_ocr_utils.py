import unittest
import cv2
import os
from src import ocr_utils, config

class TestOCRUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.img_path = os.path.join(config.RAW_DIR, 'placa.jpg')
        cls.img = cv2.imread(cls.img_path)

    def test_perform_ocr(self):
        """Teste para a função de OCR."""
        ocr_result = ocr_utils.perform_ocr(self.img)
        self.assertIsInstance(ocr_result, str, "O resultado do OCR deve ser uma string")
        self.assertGreater(len(ocr_result), 0, "O OCR deve retornar algum texto")

if __name__ == '__main__':
    unittest.main()
