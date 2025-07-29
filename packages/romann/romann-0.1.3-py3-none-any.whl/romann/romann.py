"""
romann.py - Japanese to natural romaji/English conversion library.
"""

import os
import re
import json
import jaconv
from pykakasi import kakasi
from sudachipy import tokenizer, dictionary

class RomanConverter:
    """
    RomanConverter class for converting Japanese text to natural romaji/English.
    Uses SudachiPy for morphological analysis and customizable dictionaries.
    """
    # ヘボン式ローマ字の外来語英語の辞書
    hira_dict_path = os.path.join(os.path.dirname(__file__), "hiragana_english.json")
    with open(hira_dict_path, encoding="utf-8") as f:
        HIRAGANA_ENGLISH = json.load(f)

    def __init__(self):
        """
        Initialize the RomanConverter with kakasi and SudachiPy.
        """
        self.converter = kakasi()
        # SudachiPyの初期化
        self.tokenizer_obj = dictionary.Dictionary().create()
        self.mode = tokenizer.Tokenizer.SplitMode.C  # 最も細かい分割モード

    def convert_hiragana_english(self, word: str) -> str:
        """
        Convert romanized hiragana to English if it exists in the dictionary.
        """
        return self.HIRAGANA_ENGLISH.get(word.lower(), word).capitalize()

    def _process_token(self, token) -> str:
        """Process a single token from SudachiPy."""
        surface = token.surface()

        # Handle alphanumeric tokens
        if re.match(r'^[a-zA-Z0-9]+$', surface):
            return surface

        # Get reading and convert to hiragana
        reading = token.reading_form()
        hiragana = jaconv.kata2hira(reading)

        # Check if in dictionary
        if hiragana in self.HIRAGANA_ENGLISH:
            return self.HIRAGANA_ENGLISH[hiragana]

        # Special case for particle "no"
        if surface == "の" or hiragana == "の":
            return "no"

        # Skip empty tokens
        if not surface.strip():
            return ""

        # Convert to romaji using kakasi
        romaji = self.converter.convert(surface)
        return ''.join(item['hepburn'] for item in romaji)

    def to_roman(self, text: str, remove_spaces: bool = True) -> str:
        """
        Convert Japanese text (kanji, hiragana, katakana) to romaji.
        Preserves non-Japanese characters as they are.
        Uses SudachiPy for morphological analysis to better handle loan words.

        Args:
            text (str): Input text containing Japanese characters
            remove_spaces (bool, optional): Whether to remove spaces from the output.
                Defaults to True.


        Returns:
            str: Romanized text with natural capitalization and formatting
        """
        if not text:
            return ""

        # Process tokens
        tokens = self.tokenizer_obj.tokenize(text.replace("・", " "), self.mode)
        processed_tokens = [self._process_token(token) for token in tokens]

        # Filter out empty tokens and join with spaces
        result_text = ' '.join(filter(None, processed_tokens))

        # Capitalize words and clean up spaces
        result_text = ' '.join(word.capitalize() for word in result_text.split())
        result_text = re.sub(r'\s+', ' ', result_text).strip()

        # Remove spaces if requested
        return result_text.replace(' ', '') if remove_spaces else result_text

    def _kata_to_hira(self, text: str) -> str:
        """
        カタカナをひらがなに変換する
        """
        return jaconv.kata2hira(text)
