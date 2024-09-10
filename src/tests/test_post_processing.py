import unittest
from src import post_processing

class TestPostProcessing(unittest.TestCase):

    def test_correct_ocr_text(self):
        """Teste para correção de texto OCR."""
        text = "0ABC-1234"
        corrected_text = post_processing.correct_ocr_text(text)
        self.assertEqual(corrected_text, "OABC-1234", "A função de correção de OCR não funcionou como esperado")

    def test_validate_plate_format(self):
        """Teste para validação do formato de placas."""
        valid_text = "ABC-1234"
        invalid_text = "A1B2C3"

        self.assertEqual(post_processing.validate_plate_format(valid_text), "ABC-1234", "A placa válida deveria ser detectada")
        self.assertIsNone(post_processing.validate_plate_format(invalid_text), "A placa inválida não deveria ser detectada")

if __name__ == '__main__':
    unittest.main()
