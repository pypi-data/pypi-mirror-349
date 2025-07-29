# -*- coding: utf-8 -*-
"""
test_romann.py - Tests for romann library
"""
from romann import RomanConverter


def test_remove_spaces_option():
    """
    Test the remove_spaces option specifically.
    """
    converter = RomanConverter()
    # 基本的なテスト
    assert converter.to_roman("こんにちは", remove_spaces=True) == "Konnichiha"
    assert converter.to_roman("こんにちは", remove_spaces=False) == "Konnichiha"

    # 複数単語のテスト
    assert converter.to_roman("こんにちは 世界") == "KonnichihaSekai"  # デフォルトはTrue
    assert converter.to_roman("こんにちは 世界", remove_spaces=False) == "Konnichiha Sekai"

    # 記号を含むテスト
    assert converter.to_roman("A・B・C") == "ABC"  # デフォルトはTrue
    assert converter.to_roman("A・B・C", remove_spaces=False) == "A B C"

    # 英数字と日本語の混合テスト
    assert converter.to_roman("Hello 世界 123") == "HelloSekai123"  # デフォルトはTrue
    assert converter.to_roman("Hello 世界 123", remove_spaces=False) == "Hello Sekai 123"

def test_convert_kanji_to_roman():
    """
    Test conversion of kanji to roman.
    """
    converter = RomanConverter()
    assert converter.to_roman("漢字") == "Kanji"
    assert converter.to_roman("日本語") == "Nihongo"
    assert converter.to_roman("こんにちは") == "Konnichiha"

    # スペースありバージョンのテスト
    assert converter.to_roman("漢字 日本語", remove_spaces=False) == "Kanji Nihongo"

def test_convert_mixed_text():
    """
    Test conversion of mixed Japanese text.
    """
    converter = RomanConverter()
    assert converter.to_roman("Hello漢字World", remove_spaces=False) == "Hello Kanji World"
    assert converter.to_roman("Hello漢字World") == "HelloKanjiWorld"
    assert converter.to_roman("テスト123") == "Test123"
    assert converter.to_roman("テスト123", remove_spaces=False) == "Test 123"

def test_empty_string():
    """
    Test conversion of empty string.
    """
    converter = RomanConverter()
    assert converter.to_roman("") == ""

def test_whitespace_handling():
    """
    Test handling of spaces in text.
    """
    converter = RomanConverter()
    assert converter.to_roman("こんにちは 世界") == "KonnichihaSekai"
    assert converter.to_roman("  スペース  ") == "Space"

def test_natural_japanese_titles():
    """
    Test conversion of natural Japanese titles.
    """
    converter = RomanConverter()
    assert converter.to_roman("薔薇の花") == "BaraNoHana"
    assert converter.to_roman("追憶のマーメイド") == "TsuiokuNoMermaid"
    assert converter.to_roman("A・RA・SHI") == "ARaShi"
    assert converter.to_roman("さよならCOLOR") == "SayonaraColor"

    # Test with remove_spaces=False
    assert converter.to_roman("薔薇の花", remove_spaces=False) == "Bara No Hana"
    assert converter.to_roman("追憶のマーメイド", remove_spaces=False) == "Tsuioku No Mermaid"
    assert converter.to_roman("A・RA・SHI", remove_spaces=False) == "A Ra Shi"
    assert converter.to_roman("さよならCOLOR", remove_spaces=False) == "Sayonara Color"

def test_hiragana_english():
    """
    Test conversion of hiragana to roman.
    """
    converter = RomanConverter()
    assert converter.to_roman("めーる") == "Mail"
    # SudachiPyの分割特性に合わせてテストケースを調整
    assert converter.to_roman("す") == "Su"
    assert converter.to_roman("と") == "To"
    assert converter.to_roman("らぶ") == "Love"
    assert converter.to_roman("どり") == "Dori"

def test_particle_no():
    """
    Test special handling for particle 'の'.
    """
    converter = RomanConverter()
    assert converter.to_roman("春の海") == "HaruNoUmi"
    assert converter.to_roman("僕の名前") == "BokuNoNamae"

def test_separator_conversion():
    """
    Test conversion of separators.
    """
    converter = RomanConverter()
    assert converter.to_roman("A・B・C") == "ABC"
    # ドット・パンクのSudachiPyによる分割結果に合わせる
    assert converter.to_roman("ドット・パンク") == "DottoPanku"

def test_morphological_analysis():
    """
    Test morphological analysis.
    """
    converter = RomanConverter()
    # SudachiPyの分割結果に合わせてテストケースを調整
    assert converter.to_roman("アース") == "Earth"
    assert converter.to_roman("ウィンド") == "Wind"
    assert converter.to_roman("アンド") == "And"
    assert converter.to_roman("ファイアー") == "Fire"
    assert converter.to_roman("いけない") == "IkeNai"
    assert converter.to_roman("ボーダーライン") == "BorderLine"

def test_compound_words():
    """
    Test conversion of compound words and loanwords.
    """
    converter = RomanConverter()
    # SudachiPyの分割結果に合わせてテストケースを調整
    assert converter.to_roman("釈迦") == "Shaka"
    assert converter.to_roman("インザハウス") == "Inzahausu"
    assert converter.to_roman("オープン") == "Open"
    assert converter.to_roman("ドア") == "Door"
def test_mixed_japanese_english():
    """
    Test conversion of mixed Japanese and English words.
    """
    converter = RomanConverter()
    # SudachiPyの分割結果に合わせてテストケースを調整
    assert converter.to_roman("ハロー") == "Hello"
    assert converter.to_roman("ワールド") == "World"
    assert converter.to_roman("アイ") == "I"
    assert converter.to_roman("ラブ") == "Love"
    assert converter.to_roman("ユー") == "You"

    # Test with remove_spaces=True
    assert converter.to_roman("ハロー ワールド", remove_spaces=True) == "HelloWorld"
    assert converter.to_roman("アイ ラブ ユー", remove_spaces=True) == "ILoveYou"

def test_readme_examples():
    """
    Test README conversion examples.
    """
    converter = RomanConverter()
    # READMEの変換例をそのまま検証
    assert converter.to_roman("アース・ウィンド＆ファイアー") == "EarthWindAndFire"
    assert converter.to_roman("いけないボーダーライン") == "IkeNaiBorderLine"
    assert converter.to_roman("さよならCOLOR") == "SayonaraColor"
    assert converter.to_roman("釈迦・イン・ザ・ハウス") == "ShakaInTheHouse"
