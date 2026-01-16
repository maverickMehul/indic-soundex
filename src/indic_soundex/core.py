import re
from typing import Dict, List


class IndicSoundex:
    """
    Specialized Soundex algorithm for Indian single names.
    Handles diverse phonetic patterns across Indian languages.
    """

    def __init__(self):
        # Step 1: Character normalization mappings
        self.normalize_map: Dict[str, str] = {
            # V/W variations (common in South India)
            "w": "v",
            # Q/K variations (Urdu influence)
            "q": "k",
            # F/PH variations
            "f": "ph",
            # X handling
            "x": "ks",  # Except when it represents 'ksh'
        }

        # Tamil zh ↔ l equivalence patterns
        # "zh" in Tamil is a unique retroflex approximant, often romanized as
        # "l" or "zh" interchangeably.
        self.tamil_zh_normalizations: List[tuple[str, str]] = [
            # Normalize zh+vowel patterns to l+vowel (common interchange)
            ("azha", "ala"),
            ("izhi", "ili"),
            ("uzhu", "ulu"),
            ("ezhe", "ele"),
            ("ozho", "olo"),
            ("azhi", "ali"),
            ("izha", "ila"),
            ("uzha", "ula"),
            ("ezha", "ela"),
            ("ozha", "ola"),
            # Standalone zh patterns (word boundaries)
            ("azh", "al"),
            ("izh", "il"),
            ("uzh", "ul"),
            ("ezh", "el"),
            ("ozh", "ol"),
        ]

        # Step 2: Complex phoneme mappings (process these first)
        # Order matters - longer patterns first
        self.complex_phonemes: List[tuple[str, str]] = [
            # Three character patterns
            ("ksh", "X"),
            ("sch", "S"),
            ("thr", "T"),
            # Aspirated consonants (critical for Indian names)
            ("bh", "B"),
            ("ch", "C"),
            ("dh", "D"),
            ("gh", "G"),
            ("jh", "J"),
            ("kh", "K"),
            ("ph", "P"),
            ("th", "T"),
            ("sh", "S"),
            # Double consonants (reduce to single)
            ("kk", "k"),
            ("tt", "t"),
            ("dd", "d"),
            ("nn", "n"),
            ("mm", "m"),
            ("ll", "l"),
            ("pp", "p"),
            ("bb", "b"),
            ("ss", "s"),
            ("rr", "r"),
            # Special combinations
            ("gy", "G"),
            ("ny", "N"),
            ("ng", "N"),
            ("nj", "N"),
            ("mb", "M"),
            ("nd", "N"),
            # Vowel combinations (Tamil/Telugu)
            ("aa", "a"),
            ("ee", "i"),
            ("ii", "i"),
            ("oo", "u"),
            ("uu", "u"),
            ("ai", "e"),
            ("au", "o"),
            ("ou", "o"),
            ("ei", "e"),
        ]

        # Step 3: Soundex encoding groups
        # Using distinct codes for different sound classes
        self.soundex_codes: Dict[str, str] = {
            # Vowels (0) - but keep first vowel
            "a": "0",
            "e": "0",
            "i": "0",
            "o": "0",
            "u": "0",
            "y": "0",
            # Labials (1)
            "b": "1",
            "p": "1",
            "m": "1",
            "v": "1",
            "B": "11",  # bh - aspirated
            "P": "11",  # ph - aspirated
            "M": "11",  # mb combination
            # Velars/Gutturals (2)
            "k": "2",
            "g": "2",
            "c": "2",
            "K": "22",  # kh - aspirated
            "G": "22",  # gh/gy - aspirated
            "X": "23",  # ksh - special
            # Dentals (3)
            "d": "3",
            "t": "3",
            "D": "33",  # dh - aspirated
            "T": "33",  # th/thr - aspirated
            # Palatals (4)
            "j": "4",
            "C": "44",  # ch - aspirated
            "J": "44",  # jh - aspirated
            "z": "4",  # standalone z (non-Tamil context)
            # Nasals (5)
            "n": "5",
            "N": "55",  # ng/ny/nj/nd - special nasals
            # Sibilants (6)
            "s": "6",
            "S": "66",  # sh/sch - aspirated
            # Liquids (7)
            "l": "7",
            "r": "7",
            # Aspirate/Fricative (8)
            "h": "8",
        }

        # Step 4: Ending patterns to normalize
        self.ending_patterns: List[tuple[str, str]] = [
            # Common Tamil/Telugu endings
            ("samy", "sami"),
            ("swamy", "sami"),
            ("swami", "sami"),
            ("aiah", "aya"),
            ("ayya", "aya"),
            ("amma", "ama"),
            ("appa", "apa"),
            ("anna", "ana"),
            # Tamil zh/l specific endings
            ("azhagan", "alagan"),
            ("azhagi", "alagi"),
            ("azhagiri", "alagiri"),
            ("ilzhan", "ilan"),
            ("mozhi", "moli"),
            ("thamizh", "tamil"),
            ("tamizh", "tamil"),
            # Common Hindi/Sanskrit endings
            ("anth", "ant"),
            ("endra", "inder"),
            ("chandra", "chander"),
            # Common Bengali endings
            ("erjee", "erji"),
            ("erjea", "erji"),
            ("erjie", "erji"),
            ("opadhyay", "opadyay"),
            # Common Muslim name endings
            ("uddin", "udin"),
            ("ullah", "ula"),
            ("ahmed", "ahmad"),
            ("yaz", "yaj"),
            # Simplify repeated vowel endings
            ("aa$", "a"),
            ("ee$", "i"),
            ("ii$", "i"),
            ("oo$", "u"),
            ("uu$", "u"),
        ]

    def preprocess(self, name: str) -> str:
        """Initial preprocessing of the name."""
        # Lowercase and strip
        name = name.lower().strip()

        # Remove non-alphabetic characters
        name = re.sub(r"[^a-z]", "", name)

        # Apply Tamil zh ↔ l normalizations first
        for zh_pattern, l_replacement in self.tamil_zh_normalizations:
            name = name.replace(zh_pattern, l_replacement)

        # Apply character normalizations
        for old, new in self.normalize_map.items():
            name = name.replace(old, new)

        # Apply ending normalizations
        for pattern, replacement in self.ending_patterns:
            if pattern.endswith("$"):
                name = re.sub(pattern, replacement, name)
            elif name.endswith(pattern):
                name = name[: -len(pattern)] + replacement

        return name

    def apply_complex_phonemes(self, name: str) -> str:
        """Replace complex phonemes with single character markers."""
        for phoneme, marker in self.complex_phonemes:
            name = name.replace(phoneme, marker)
        return name

    def encode(self, name: str, length: int = 4, extended: bool = False) -> str:
        """
        Encode name to Soundex code.

        Args:
            name: Single name to encode.
            length: Output code length (default 4).
            extended: If True, uses two-digit codes for aspirated sounds.

        Returns:
            Soundex code string.
        """
        if not name:
            return "0" * length

        # Preprocess
        processed = self.preprocess(name)
        if not processed:
            return "0" * length

        # Apply complex phoneme replacements
        processed = self.apply_complex_phonemes(processed)

        # Keep original first character (important for Indian names)
        first_char = processed[0].upper()
        code = first_char

        # Track last code to avoid repetition
        last_code = ""

        # Process remaining characters
        for char in processed[1:]:
            if char in self.soundex_codes:
                char_code = self.soundex_codes[char]

                # Skip vowels (0)
                if char_code == "0":
                    continue

                # Skip if same as last code (avoid repetition)
                if char_code != last_code:
                    if extended or len(char_code) == 1:
                        code += char_code
                    else:
                        # For non-extended mode, use single digit
                        code += char_code[0]
                    last_code = char_code

            # Stop if we've reached desired length
            if not extended and len(code) >= length:
                break

        # Pad with zeros if needed
        if len(code) < length:
            code += "0" * (length - len(code))

        return code[:length] if not extended else code
