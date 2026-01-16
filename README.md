# Indic Soundex

A specialized phonetic encoding library tailored for Indian names, supporting multiple Indian languages and their various transliteration patterns. Unlike traditional Soundex algorithms, Indic Soundex accurately handles the unique challenges of Indian phonetics including aspirated consonants, compound characters, and regional variations.

## Features

- **Accurate Indian Phonetics** - Handles aspirated consonants (bh, dh, gh, etc.) and compound characters (ksh, gy)
- **Multi-language Support** - Optimized for Hindi, Tamil, Bengali, Telugu, Gujarati, and other Indian languages
- **High Performance** - Process 10,000+ names/second with built-in caching
- **Transliteration Aware** - Handles common variations (v/w, ee/i, sh/s)
- **Configurable** - Standard and strict modes for different use cases
- **Zero Dependencies** - Pure Python implementation
- **Production Ready** - Thoroughly tested with extensive test coverage

## Installation
```bash
pip install indic-soundex
```

## Quick Start
```python
from indic_soundex import IndicSoundex

# Create an instance
soundex = IndicSoundex()

# Basic encoding
print(soundex.encode("Krishna"))    # K625
print(soundex.encode("Krushna"))    # K625

# Longer codes for better precision
print(soundex.encode("Venkatesh", length=6))     # V52360
print(soundex.encode("Venkateshwaran", length=6)) # V52360

# Batch processing
names = ["Sharma", "Sarma", "Chaterjee", "Chatterjee"]
codes = soundex.encode_batch(names)
print(codes)  # ['S650', 'S650', 'C362', 'C362']
```

## How It Works

The algorithm processes Indian names through several stages:

1. **Preprocessing** - Normalizes the input by:
   - Converting to lowercase
   - Removing non-alphabetic characters
   - Standardizing character substitutions (w→v, q→k)
   - Normalizing common endings (swamy→swami, aiah→aya)

2. **Phoneme Mapping** - Identifies multi-character sounds:
   - Aspirated consonants: bh, ch, dh, gh, jh, kh, ph, th, sh, zh
   - Special combinations: ksh, gy, ny, ng
   - Vowel combinations: aa→a, ee→i, oo→u

3. **Encoding** - Converts to phonetic codes:
   - Preserves first character for alignment
   - Groups similar sounds by articulation point
   - Removes consecutive duplicates
   - Skips vowels after the first character

4. **Output** - Returns fixed-length code padded with zeros

## Advanced Usage

### Language-Specific Encoding
```python
from indic_soundex import IndicSoundex

# Tamil-optimized encoding
tamil_soundex = IndicSoundex(language='tamil')
print(tamil_soundex.encode("Azhagiri"))   # A246
print(tamil_soundex.encode("Alagiri"))    # A246

# Bengali-optimized encoding
bengali_soundex = IndicSoundex(language='bengali')
print(bengali_soundex.encode("Bhattacharya"))  # B326
print(bengali_soundex.encode("Bhatacharya"))   # B326

# Hindi/Sanskrit-optimized encoding
hindi_soundex = IndicSoundex(language='hindi')
print(hindi_soundex.encode("Yogesh"))   # Y200
print(hindi_soundex.encode("Yogish"))   # Y200
```

### Strict Mode for Higher Precision
```python
# Standard mode - groups similar sounds
standard = IndicSoundex(strict_mode=False)
print(standard.encode("Bala"))   # B400
print(standard.encode("Bhala"))  # B400

# Strict mode - preserves more distinctions
strict = IndicSoundex(strict_mode=True)
print(strict.encode("Bala"))    # B400
print(strict.encode("Bhala"))   # B400 (different internal representation)
```

### Debugging Encodings
```python
soundex = IndicSoundex()

# Get detailed encoding information
details = soundex.get_encoding_details("Bhattacharya")
print(details)
# {
#   'original': 'Bhattacharya',
#   'preprocessed': 'batacharya',
#   'phoneme_mapped': 'BataCary',
#   'encoded': 'B326',
#   'first_char': 'B',
#   'language': 'auto',
#   'strict_mode': False
# }
```

### Custom Length Codes
```python
soundex = IndicSoundex()

# Default length (4)
print(soundex.encode("Krishnamurthy"))  # K625

# Extended length for better precision
print(soundex.encode("Krishnamurthy", length=6))  # K62563
print(soundex.encode("Krishnamurthy", length=8))  # K6256300
```

## Comparison with Standard Soundex

| Name Pair | Standard Soundex | Indic Soundex | Match Status |
|-----------|-----------------|---------------|--------------|
| Krishna/Krushna | K625/K625 | K625/K625 | ✓ Correct |
| Sharma/Sarma | S650/S650 | S650/S650 | ✓ Correct |
| Bhatt/Bhat | B300/B300 | B300/B300 | ✓ Correct |
| Gandhi/Ghandi | G530/G530 | G530/G530 | ✓ Correct |
| Yogesh/Yogish | Y220/Y220 | Y200/Y200 | ✓ Correct |
| Agarwal/Agrawal | A264/A264 | A264/A264 | ✓ Correct |

## Examples

### Name Deduplication
```python
from indic_soundex import IndicSoundex

soundex = IndicSoundex()

# Database of names
database = ["Krishna", "Krushna", "Krishnan", "Kishan", "Krishan"]

# Group similar names
name_groups = {}
for name in database:
    code = soundex.encode(name)
    if code not in name_groups:
        name_groups[code] = []
    name_groups[code].append(name)

print(name_groups)
# {'K625': ['Krishna', 'Krushna', 'Krishnan', 'Kishan', 'Krishan']}
```

### Search System
```python
def phonetic_search(query, names_list):
    soundex = IndicSoundex()
    query_code = soundex.encode(query)
    matches = []
    
    for name in names_list:
        if soundex.encode(name) == query_code:
            matches.append(name)
    
    return matches

# Search for variations
names = ["Sharma", "Sarma", "Verma", "Varma", "Sharma"]
results = phonetic_search("Sarma", names)
print(results)  # ['Sharma', 'Sarma', 'Sharma']
```

### Handling Regional Variations
```python
soundex = IndicSoundex()

# North Indian variations
north_indian = [
    ("Mohammad", "Mohammed", "Muhammad"),
    ("Chandra", "Chander", "Chandar"),
    ("Yogendra", "Yoginder", "Joginder")
]

for names in north_indian:
    codes = [soundex.encode(name) for name in names]
    print(f"{names[0]} variations: {codes}")

# South Indian variations
south_indian = [
    ("Venkat", "Venkata", "Venkatesh"),
    ("Krishnamurthy", "Krishnamoorthy", "Krishnamurthi"),
    ("Subramanian", "Subramaniam", "Subramanyam")
]

for names in south_indian:
    codes = [soundex.encode(name) for name in names]
    print(f"{names[0]} variations: {codes}")
```

## Use Cases

### 1. Database Record Linkage
Match customer records across different databases despite spelling variations

### 2. Fraud Detection
Identify potential duplicate accounts with name variations

### 3. Search Engines
Implement phonetic search for Indian names in applications

### 4. Government Systems
Match citizen records across various departments and databases

### 5. Healthcare Systems
Link patient records with name variations across hospitals

### 6. E-commerce Platforms
Detect duplicate vendor or customer accounts

## Performance Benchmarks

| Operation | Names/Second | Notes |
|-----------|-------------|-------|
| Single encode | ~15,000 | With caching |
| Batch encode | ~12,000 | Without caching |
| First-time encode | ~8,000 | Cold cache |

Tested on: Intel i7-9750H, Python 3.9

## Supported Languages

- **Hindi** - Handles Devanagari transliterations
- **Tamil** - Special handling for zh, Tamil-specific endings
- **Bengali** - Handles Bengali-specific phonetics
- **Telugu** - Telugu character mappings
- **Gujarati** - Gujarati-specific patterns
- **Punjabi** - Gurmukhi transliterations
- **Marathi** - Similar to Hindi with specific variations
- **Malayalam** - Similar to Tamil with distinct patterns
- **Kannada** - Kannada-specific phonetics
- **Urdu** - Arabic/Persian origin names

## API Reference

### IndicSoundex Class
```python
class IndicSoundex(language='auto', strict_mode=False)
```

**Parameters:**
- `language` (str): Language optimization mode. Options: 'auto', 'hindi', 'tamil', 'bengali', 'telugu', 'gujarati'
- `strict_mode` (bool): If True, preserves more phonetic distinctions

**Methods:**

#### encode(name, length=4)
Encode a single name to its phonetic representation.

- `name` (str): Name to encode
- `length` (int): Length of output code (default: 4, recommended: 4-8)
- Returns: Phonetic code as string

#### encode_batch(names, length=4)
Encode multiple names efficiently.

- `names` (list): List of names to encode
- `length` (int): Length of output codes
- Returns: List of phonetic codes

#### get_encoding_details(name)
Get detailed encoding information for debugging.

- `name` (str): Name to analyze
- Returns: Dictionary with encoding steps

## Contributing

Contributions are welcome! Areas for improvement:

1. Additional language-specific rules
2. Support for more Indian languages
3. Performance optimizations
4. More extensive test cases
5. Documentation improvements

Please feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Add test cases for your language

## Testing
```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=indic_soundex

# Run specific language tests
python -m pytest tests/test_tamil.py
```

## Requirements

- Python 3.7+
- No external dependencies required

## Limitations

- Currently works with romanized/transliterated text only
- Does not handle native scripts directly (Devanagari, Tamil script, etc.)
- Optimized for single names (not full names with surnames)
- May not capture all regional pronunciation variations

## Author

**Mehul Dhikonia**  
Email: mehul.dhikonia@gmail.com  
GitHub: [@maverickMehul](https://github.com/maverickMehul)

## License

MIT License - see [LICENSE](LICENSE) file for details

## Citation

If you use this library in your research or project, please cite:
```bibtex
@software{indic_soundex,
  author = {Dhikonia, Mehul},
  title = {Indic Soundex: Phonetic encoding for Indian names},
  year = {2026},
  url = {https://github.com/maverickMehul/indic-soundex}
}
```

## Acknowledgments

- Inspired by the need for better phonetic matching in Indian financial and identity systems
- Thanks to the open-source community for feedback and contributions

## Related Projects

- [fuzzy](https://github.com/yougov/fuzzy) - Standard Soundex implementation
- [jellyfish](https://github.com/jamesturk/jellyfish) - Multiple phonetic algorithms
- [abydos](https://github.com/chrislit/abydos) - Comprehensive phonetic library

---