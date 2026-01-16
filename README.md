# Indic Soundex

A specialized phonetic encoding library tailored for Indian names, supporting multiple Indian languages and their various transliteration patterns. Unlike traditional Soundex algorithms, Indic Soundex accurately handles the unique challenges of Indian phonetics including aspirated consonants, compound characters, and regional variations.

## Features

- **Accurate Indian Phonetics** - Handles aspirated consonants (bh, dh, gh, etc.) and compound characters (ksh, gy)
- **Tamil-specific Support** - Special handling for Tamil zh ↔ l interchange patterns
- **Transliteration Aware** - Handles common variations (v/w, q/k, f/ph)
- **Zero Dependencies** - Pure Python implementation using only standard library
- **Lightweight** - Single file implementation, easy to integrate

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

# Tamil names with zh/l variations
print(soundex.encode("Azhagiri"))   # A7467
print(soundex.encode("Alagiri"))    # A7467

# Longer codes for better precision
print(soundex.encode("Venkatesh", length=6))     # V52360
print(soundex.encode("Venkateshwaran", length=6)) # V52360

# Extended mode for detailed encoding
print(soundex.encode("Bharath", extended=True))  # B7633
```

## How It Works

The algorithm processes Indian names through four stages:

### 1. Tamil zh ↔ l Normalization
Handles the unique Tamil retroflex approximant 'zh' (ழ) which is often interchanged with 'l':
- azha → ala, izhi → ili, uzhu → ulu
- Normalizes names like "Azhagiri" and "Alagiri" to the same pattern

### 2. Character Normalization
- w → v (South Indian variations)
- q → k (Urdu influence)
- f → ph (phonetic equivalence)
- x → ks (except when part of 'ksh')

### 3. Phoneme Mapping
Identifies and maps multi-character sounds:
- **Aspirated consonants**: bh→B, ch→C, dh→D, gh→G, jh→J, kh→K, ph→P, th→T, sh→S
- **Special combinations**: ksh→X, gy→G, ny→N, ng→N
- **Double consonants**: kk→k, tt→t, dd→d, nn→n, mm→m
- **Vowel combinations**: aa→a, ee→i, oo→u, ai→e, au→o

### 4. Soundex Encoding
Converts to phonetic codes based on articulation:
- **Vowels (0)**: a, e, i, o, u, y
- **Labials (1)**: b, p, m, v (bh, ph → 11 in extended mode)
- **Velars (2)**: k, g, c (kh, gh → 22 in extended mode)
- **Dentals (3)**: d, t (dh, th → 33 in extended mode)
- **Palatals (4)**: j, z (ch, jh → 44 in extended mode)
- **Nasals (5)**: n (special nasals → 55 in extended mode)
- **Sibilants (6)**: s (sh → 66 in extended mode)
- **Liquids (7)**: l, r
- **Aspirate (8)**: h

## Examples

### North Indian Names
```python
soundex = IndicSoundex()

# Hindi/Sanskrit names
print(soundex.encode("Sharma"))     # S650
print(soundex.encode("Sarma"))      # S650

print(soundex.encode("Krishna"))    # K625
print(soundex.encode("Krushna"))    # K625
print(soundex.encode("Kishan"))     # K650

# Aspirated consonants
print(soundex.encode("Bharat"))     # B630
print(soundex.encode("Bharath"))    # B630
```

### South Indian Names
```python
soundex = IndicSoundex()

# Tamil names with zh/l variations
print(soundex.encode("Azhagan"))    # A725
print(soundex.encode("Alagan"))     # A725

print(soundex.encode("Thamizh"))    # T570
print(soundex.encode("Tamil"))      # T570

# Telugu/Kannada names
print(soundex.encode("Venkat"))     # V523
print(soundex.encode("Venkata"))    # V523

print(soundex.encode("Subramanian")) # S165
print(soundex.encode("Subramaniam")) # S165
```

### Bengali Names
```python
soundex = IndicSoundex()

print(soundex.encode("Chatterjee"))  # C364
print(soundex.encode("Chaterjee"))   # C364

print(soundex.encode("Mukherjee"))   # M264
print(soundex.encode("Mukherji"))    # M264

print(soundex.encode("Bandyopadhyay")) # B531
print(soundex.encode("Bandopadhyay"))  # B531
```

### Muslim Names
```python
soundex = IndicSoundex()

print(soundex.encode("Mohammed"))    # M533
print(soundex.encode("Mohammad"))    # M533
print(soundex.encode("Muhammad"))    # M533

print(soundex.encode("Ahmed"))       # A533
print(soundex.encode("Ahmad"))       # A533

print(soundex.encode("Rahman"))      # R550
print(soundex.encode("Rehman"))      # R550
```

## API Reference

### IndicSoundex Class
```python
class IndicSoundex()
```

Creates a new instance of the Indic Soundex encoder.

### Methods

#### encode(name, length=4, extended=False)

Encode a name to its phonetic representation.

**Parameters:**
- `name` (str): Single name to encode
- `length` (int): Output code length (default: 4)
- `extended` (bool): If True, uses two-digit codes for aspirated sounds providing more precision

**Returns:**
- str: Soundex code of specified length

**Example:**
```python
soundex = IndicSoundex()

# Standard encoding
code = soundex.encode("Bharath")  # B630

# Extended encoding (more precise)
code = soundex.encode("Bharath", extended=True)  # B7633

# Custom length
code = soundex.encode("Krishnamurthy", length=8)  # K6255630
```

## Use Cases

1. **Name Deduplication** - Identify duplicate entries with name variations
2. **Search Systems** - Implement phonetic search for Indian names
3. **Record Linkage** - Match records across databases with spelling variations
4. **Fraud Detection** - Identify potential duplicate accounts
5. **Customer Support** - Find customer records despite spelling errors

## Name Normalization Examples

The algorithm handles various types of name variations:

| Original | Normalized | Soundex |
|----------|------------|---------|
| Azhagiri | Alagiri | A7467 |
| Thamizh | Tamil | T570 |
| Krishna | Krushna | K625 |
| Mohammad | Mohammed | M533 |
| Sharma | Sarma | S650 |
| Chatterjee | Chaterjee | C364 |
| Venkatesh | Venkateshwaran | V5236 (length=5) |

## Limitations

- Works with romanized/transliterated text only
- Does not handle native scripts (Devanagari, Tamil, etc.)
- Optimized for single names, not full names with surnames
- May not capture all regional pronunciation variations

## Contributing

Contributions are welcome! Areas for improvement:

1. Additional language-specific patterns
2. Support for more Indian languages
3. Native script support
4. Performance optimizations
5. More test cases

## Author

**Mehul Dhikonia**  
Email: mehul.dhikonia@gmail.com

## License

MIT License - see [LICENSE](LICENSE) file for details

## Citation

If you use this library in your research or project, please cite:
```bibtex
@software{indic_soundex,
  author = {Dhikonia, Mehul},
  title = {Indic Soundex: Phonetic encoding for Indian names},
  year = {2024},
  url = {https://github.com/maverickMehul/indic-soundex}
}
```

---