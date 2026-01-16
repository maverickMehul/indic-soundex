"""
Compatibility shim for the legacy module path.

Prefer importing from the package:
    from indic_soundex import IndicSoundex
"""

from indic_soundex.core import IndicSoundex

__all__ = ["IndicSoundex"]