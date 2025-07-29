# romann

日本語テキストを自然なローマ字や英語表記に変換するPythonライブラリです。
曲名・人名・外来語などを、視認性の高いローマ字や本来のスペルで出力します。
液晶ディスプレイや海外向け表示などにご活用いただけます。

## 主な特徴

- SudachiPyによる高精度な形態素解析
- 外来語は辞書に基づき英語表記に自動変換（カスタマイズ可）
- 4x8ドット液晶でも読みやすいローマ字表記
- Python 3.12対応・TDDによる品質管理

## 変換例

| 日本語 | ローマ字 | 英語表記 |
|:--|:--|:--|
| アース・ウィンド＆ファイアー | Aasu Wind & Faiaa | Earth Wind And Fire |
| いけないボーダーライン | Ikenai Boodaa Rain | Ikenai Border Line |
| さよならCOLOR | Sayonara Color | Sayonara Color |
| 釈迦・イン・ザ・ハウス | Shaka In Za Hausu | Shaka In The House |

## 動作環境

- Python 3.12
- 主要依存: SudachiPy, pykakasi, jaconv

## インストール

```bash
pip install romann
```

## 使い方

```python
from romann import RomanConverter
converter = RomanConverter()
print(converter.to_roman("薔薇の花"))  # BaraNoHana
print(converter.to_roman("アース・ウィンド＆ファイアー"))  # EarthWindAndFire

# スペースありの変換（オプション）
print(converter.to_roman("薔薇の花", remove_spaces=False))  # Bara No Hana
print(converter.to_roman("アース・ウィンド＆ファイアー", remove_spaces=False))  # Earth Wind & Fire
```

## 変換ルール

- 単語の先頭は大文字
- デフォルトではスペースなしで出力（オプションでスペース区切りに変更可能）
- 外来語は辞書にあれば英語表記、なければローマ字
- 記号類はそのまま（「、」「。」は「,」「.」に変換）
- 前後・連続する空白は整理

## 外来語辞書のカスタマイズ

外来語の変換は `hiragana_english.json` および `katakana_english.json` に基づきます。
これらを編集することで、特定単語の変換方法を調整できます。

例（hiragana_english.json）:
```json
{
  "あーす": "earth",
  "どあ": "door"
}
```
- hiragana_english.json: ひらがな→英語表記
- katakana_english.json: カタカナ→英語表記

## 関連

- [Kanjiconv](https://zenn.dev/sea_turt1e/articles/e7dc022231a86c)

---

ご利用・フィードバック・Issue歓迎します。
- 連続する空白は1つの空白に変換

## インストール

```bash
pip install romann
```

## 依存ライブラリ

- pykakasi: 日本語のローマ字変換
- SudachiPy: 形態素解析
- jaconv: 文字コード変換

## 使用方法

```python
from romann import RomanConverter

converter = RomanConverter()

# 日本語テキストをローマ字に変換
text = "薔薇の花"
romaji = converter.to_roman(text)
print(romaji)  # 出力: "Bara No Hana"

# 外来語を含むテキストの変換
text = "アースウィンド"
romaji = converter.to_roman(text)
print(romaji)  # 出力: "Earth Wind"
```

## 外来語辞書のカスタマイズ

外来語の変換は `hiragana_english.json` ファイルに基づいて行われます。このファイルをカスタマイズすることで、特定の単語の変換方法を調整できます。

```json
{
  "あーす": "earth",
  "どあ": "door",
  "らぶ": "love"
}
```

## 使用例

```python
from romann import RomanConverter

converter = RomanConverter()

# 通常の変換（スペースなし）
result = converter.to_roman("こんにちは")
print(result)  # 出力: Konnichiha

# 複数単語の変換（デフォルトでスペースなし）
result = converter.to_roman("こんにちは 世界")
print(result)  # 出力: KonnichihaSekai

# スペースありの変換
result = converter.to_roman("こんにちは 世界", remove_spaces=False)
print(result)  # 出力: Konnichiha Sekai
```

## 関連

* [Kanjiconv](https://zenn.dev/sea_turt1e/articles/e7dc022231a86c)
