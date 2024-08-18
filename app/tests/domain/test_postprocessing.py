import unittest
from domain.postprocessing.models import TranslatePostProcessing

class TestTranslatePostProcessing(unittest.TestCase):

    def test_translate_korean(self):
        # Given
        input_text = "안녕하세요"
        lang = 0
        
        # When
        result = TranslatePostProcessing.do_process(input_text, lang=lang)
        
        # Then
        assert result == input_text

    def test_translate_english(self):
        # Given
        input_text = "안녕하세요"
        lang = 1
        
        # When
        result = TranslatePostProcessing.do_process(input_text, lang=lang)
        
        # Then
        # Assuming the translation logic is to be implemented, for now we expect the same input as output.
        assert result == input_text

    def test_translate_invalid_lang(self):
        # Given
        input_text = "안녕하세요"
        lang = 2
        
        # When / Then
        with self.assertRaises(ValueError) as context:
            TranslatePostProcessing.do_process(input_text, lang=lang)
        assert "lang argument one choice" in str(context.exception)

    def test_translate_invalid_input_type(self):
        # Given
        input_data = 123  # Not a string
        
        # When / Then
        with self.assertRaises(ValueError) as context:
            TranslatePostProcessing.do_process(input_data, lang=1)
        assert "Input value only expected type str" in str(context.exception)

