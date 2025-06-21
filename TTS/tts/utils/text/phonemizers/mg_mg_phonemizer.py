from typing import Dict

from TTS.tts.utils.text.malagasy.phonemizer import malagasy_text_to_phonemes
from TTS.tts.utils.text.phonemizers.base import BasePhonemizer

_DEF_MG_PUNCS = ".,[]()?!'-"

class MG_MG_Phonemizer(BasePhonemizer):
    """🐸TTS Mg-Mg phonemizer using functions from the Malagasy phonemizer script.

    Example:
        >>> from TTS.tts.utils.text.phonemizers import MG_MG_Phonemizer
        >>> phonemizer = MG_MG_Phonemizer()
        >>> phonemizer.phonemize("Salama tompoko, manao ahoana ianao?", separator="|")
        's|a|l|a|m|a|t|u|m|p|u|k|u|,|m|a|n|o|o|h|u|a|n|a|i|n|a|o|?'
    """

    language = "mg-mg"

    def __init__(self, punctuations=_DEF_MG_PUNCS, keep_puncs=True, **kwargs):  # pylint: disable=unused-argument
        super().__init__(self.language, punctuations=punctuations, keep_puncs=keep_puncs)

    @staticmethod
    def name() -> str:
        """Returns the unique name of the phonemizer."""
        return "mg_mg_phonemizer"

    def _phonemize(self, text: str, separator: str = "|") -> str:
        """
        Converts text to a string of phonemes.
        Our underlying function returns space-separated phonemes,
        so we split them and join with the desired separator.
        """
        # Get the space-separated phoneme string
        phonemes_str = malagasy_text_to_phonemes(text)
        
        # Split into a list of phonemes
        phonemes_list = phonemes_str.split()

        if separator is not None and separator != "":
            return separator.join(phonemes_list)
            
        # If no separator, return a concatenated string
        return "".join(phonemes_list)

    def phonemize(self, text: str, separator="|", language=None) -> str:
        """
        Custom phonemize for mg-mg.
        This overrides the base method to skip pre- and post-processing steps,
        similar to the ja-jp implementation.
        """
        return self._phonemize(text, separator)

    @staticmethod
    def supported_languages() -> Dict:
        """Returns a dictionary of supported languages and their names."""
        return {"mg-mg": "Malagasy (Madagascar)"}

    def version(self) -> str:
        """Returns the phonemizer version."""
        return "0.0.1"

    def is_available(self) -> bool:
        """Returns True if the phonemizer is available."""
        return True


# Example usage:
if __name__ == "__main__":
    text = "Salama tompoko, manao ahoana ianao?"
    e = MG_MG_Phonemizer()
    print(f"Supported Languages: {e.supported_languages()}")
    print(f"Version: {e.version()}")
    print(f"Language: {e.language}")
    print(f"Name: {e.name()}")
    print(f"Is Available: {e.is_available()}")
    print(f"Phonemized text: `{e.phonemize(text)}`")
    
    text_with_number = "Ny vidin'ny boky iray dia Ar 5,000."
    print(f"Phonemized text with numbers: `{e.phonemize(text_with_number)}`")

