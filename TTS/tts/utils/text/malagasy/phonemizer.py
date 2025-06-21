# phonemizer.py
#
# This script converts Malagasy text to phonemes.
# It is designed to be a starting point for integrating Malagasy
# language support into a Text-to-Speech (TTS) pipeline.

import re
import unicodedata
# The `num2words` library is not used because it does not support Malagasy ('mg'),
# which caused a NotImplementedError.

# Grapheme-to-phoneme conversion rules for Malagasy.
# This list includes single letters, digraphs, and trigraphs.
_CONVRULES = [
    # Digraphs and Trigraphs
    "ao/o",
    "ai/aj",
    "ay/aj",
    "dr/ɖr",
    "tr/ʈr",
    "ts/ts",
    "mb/ᵐb",
    "mp/ᵐp",
    "nd/ⁿd",
    "nt/ⁿt",
    "ng/ᵑɡ",
    "nk/ᵑk",
    "nj/ⁿdz",
    "oa/o",
    "oi/uj",
    "oy/uj",
    # Single Letters
    "a/a",
    "b/b",
    "d/d",
    "e/e",
    "f/f",
    "g/ɡ",
    "h/h",
    "i/i",
    "j/dz",
    "k/k",
    "l/l",
    "m/m",
    "n/n",
    "o/u", # Note: 'o' is pronounced as /u/ in Malagasy
    "p/p",
    "r/r",
    "s/s",
    "t/t",
    "v/v",
    "y/i", # Note: 'y' is pronounced as /i/
    "z/z",
    # Symbols
    "、/,",
    "。/.",
    "！/!",
    "？/?",
    "・/,",
    "'/ '", # Apostrophe for contractions
    "-/ - ", # Hyphen
]

def _makerulemap():
    """Creates a tuple of dictionaries for 1, 2, and 3-character rules."""
    rules = [tuple(x.split("/")) for x in _CONVRULES]
    max_len = max(len(k) for k, v in rules)
    rule_maps = []
    for i in range(1, max_len + 1):
        rule_maps.append({k: v for k, v in rules if len(k) == i})
    return tuple(reversed(rule_maps)) # Process longest matches first


_RULEMAPS = _makerulemap()


def mg_grapheme_to_phoneme(text: str) -> str:
    """
    Convert Malagasy text (graphemes) to phonemes.
    The text is expected to be normalized and cleaned.
    """
    text = text.strip().lower()
    res = ""
    while text:
        matched = False
        # Iterate through rule maps from longest to shortest key
        for rulemap in _RULEMAPS:
            if not rulemap:
                continue
            key_len = len(next(iter(rulemap)))
            if len(text) >= key_len:
                key = text[:key_len]
                phoneme = rulemap.get(key)
                if phoneme is not None:
                    res += " " + phoneme
                    text = text[key_len:]
                    matched = True
                    break
        if not matched:
            # If no rule matches, keep the character and move to the next
            res += " " + text[0]
            text = text[1:]

    return res.strip()


def _number_to_malagasy_digits(number_str: str) -> str:
    """
    Converts a number string (e.g., "2025") into a string of
    Malagasy words for each digit ("roa aotra roa dimy").
    """
    digit_map = {
        '0': 'aotra', '1': 'iray', '2': 'roa', '3': 'telo', '4': 'efatra',
        '5': 'dimy', '6': 'enina', '7': 'fito', '8': 'valo', '9': 'sivy',
        '.': 'teboka'  # For decimal points
    }
    return ' '.join(digit_map.get(digit, '') for digit in number_str).strip()


_NUMBER_RX = re.compile(r"[0-9]+(\.[0-9]+)?")
_CURRENCY_MAP = {"$": "dôlara", "€": "euro", "Ar": "ariary"}
_CURRENCY_RX = re.compile(r"([$€]|Ar)([0-9.,]*[0-9])")


def malagasy_convert_numbers_to_words(text: str) -> str:
    """
    Converts numbers and currency symbols in a Malagasy text to their word form.
    Handles common currency symbols and the local currency 'Ariary'.
    NOTE: The num2words library does not support Malagasy. This function will
    convert numbers by spelling out each digit individually.
    """
    # Replace thousand separators
    res = re.sub(r"([0-9]),([0-9])", r"\1\2", text)
    # Handle currency (e.g., "Ar 5,000" -> "5000 ariary")
    res = _CURRENCY_RX.sub(lambda m: m[2].replace(",", "") + " " + _CURRENCY_MAP.get(m[1], m[1]), res)
    # Convert remaining numbers to words by spelling digits
    res = _NUMBER_RX.sub(lambda m: _number_to_malagasy_digits(m[0]), res)
    return res


def malagasy_text_to_phonemes(text: str) -> str:
    """
    Main function to convert a string of Malagasy text into its phonemic representation.
    Pipeline:
    1. Normalize text to NFKC form.
    2. Convert numbers to words.
    3. Convert graphemes to phonemes.
    """
    # Normalize unicode characters
    res = unicodedata.normalize("NFKC", text)
    # Convert numbers and currency to words
    res = malagasy_convert_numbers_to_words(res)
    # Convert the processed text to phonemes
    res = mg_grapheme_to_phoneme(res)

    # Basic post-processing to clean up spaces
    res = re.sub(r"\s+", " ", res).strip()
    return res

# --- Example Usage ---
if __name__ == "__main__":
    # Example sentences in Malagasy
    text1 = "Salama tompoko, manao ahoana ianao?"
    text2 = "Ny vidin'ny boky iray dia Ar 5,000."
    text3 = "Amin'ny 2025 isika no handeha."
    text4 = "Trondro sy vary no sakafo." # Contains digraphs

    print(f"Original: '{text1}'")
    phonemes1 = malagasy_text_to_phonemes(text1)
    print(f"Phonemes: {phonemes1}\n")

    print(f"Original: '{text2}'")
    phonemes2 = malagasy_text_to_phonemes(text2)
    print(f"Phonemes: {phonemes2}\n")

    print(f"Original: '{text3}'")
    phonemes3 = malagasy_text_to_phonemes(text3)
    print(f"Phonemes: {phonemes3}\n")

    print(f"Original: '{text4}'")
    phonemes4 = malagasy_text_to_phonemes(text4)
    print(f"Phonemes: {phonemes4}\n")
