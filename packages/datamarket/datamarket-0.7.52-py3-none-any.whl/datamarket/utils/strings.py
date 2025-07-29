########################################################################################################################
# IMPORTS

from enum import Enum, auto
from typing import Any
import unicodedata

import numpy as np
from unidecode import unidecode
from inflection import parameterize, underscore, titleize, camelize
from string_utils import prettify, strip_html

########################################################################################################################
# CLASSES


class NormalizationMode(Enum):
    NONE = auto()
    BASIC = auto()  # removes accents and converts punctuation to spaces
    SYMBOLS = auto()  # translates only symbols to Unicode name
    FULL = auto()  # BASIC + SYMBOLS


class NamingConvention(Enum):
    NONE = auto()  # no style change
    CONSTANT = auto()  # CONSTANT_CASE (uppercase, underscores)
    SNAKE = auto()  # snake_case (lowercase, underscores)
    CAMEL = auto()  # camelCase (capitalize words except first one, no spaces)
    PASCAL = auto()  # PascalCase (capitalize words including first one, no spaces)
    PARAM = auto()  # parameterize (hyphens)
    TITLE = auto()  # titleize (capitalize words)


########################################################################################################################
# FUNCTIONS


def transliterate_symbols(s: str) -> str:
    """
    Translates symbols (category S*) to lowercase Unicode names,
    with spaces→underscores. The rest of the text remains the same.
    """
    out: list[str] = []
    for c in s:
        if unicodedata.category(c).startswith("S"):
            name = unicodedata.name(c, "")
            if name:
                out.append(name.lower().replace(" ", "_"))
        else:
            out.append(c)
    return "".join(out)


def normalize(
    s: Any, mode: NormalizationMode = NormalizationMode.BASIC, naming: NamingConvention = NamingConvention.NONE
) -> str:
    """
    1. Normalizes the string according to `mode`:
       - NONE: returns the original input as an unprocessed string.
       - BASIC: removes accents, converts punctuation to spaces, preserves alphanumeric characters.
       - SYMBOLS: translates only symbols to Unicode name.
       - FULL: combines BASIC + SYMBOLS.
    2. Applies naming convention according to `naming`:
       - NONE: returns the normalized text.
       - PARAM: parameterize (hyphens).
       - SNAKE: snake_case (underscore, lowercase).
       - CONSTANT: CONSTANT_CASE (underscore, uppercase).
    """
    # Parameter mapping
    if isinstance(mode, str):
        mode = NormalizationMode[mode]
    if isinstance(naming, str):
        naming = NamingConvention[naming]

    # Handling null values
    if s is None or (isinstance(s, float) and np.isnan(s)):
        normalized = ""
    elif not isinstance(s, str):
        return str(s)
    else:
        text = prettify(strip_html(str(s), True))
        if mode is NormalizationMode.NONE:
            normalized = text
        elif mode is NormalizationMode.SYMBOLS:
            normalized = transliterate_symbols(text)
        else:
            # BASIC and FULL: remove accents and lowercase
            normalized = unidecode(text).lower()
            tokens: list[str] = []
            current: list[str] = []

            def flush_current():
                nonlocal current
                if current:
                    tokens.append("".join(current))
                    current.clear()

            for c in normalized:
                cat = unicodedata.category(c)
                if c.isalnum():
                    current.append(c)
                elif mode is NormalizationMode.FULL and cat.startswith("S"):
                    flush_current()
                    name = unicodedata.name(c, "")
                    if name:
                        tokens.append(name.lower().replace(" ", "_"))
                elif cat.startswith("P") or c.isspace():
                    flush_current()
                # other characters ignored

            flush_current()
            normalized = " ".join(tokens)

    # Apply naming convention
    if naming is NamingConvention.NONE:
        return normalized
    if naming is NamingConvention.PARAM:
        return parameterize(normalized)
    if naming is NamingConvention.TITLE:
        return titleize(normalized)

    underscored = underscore(parameterize(normalized))
    if naming is NamingConvention.CONSTANT:
        return underscored.upper()
    if naming is NamingConvention.CAMEL:
        return camelize(underscored, False)
    if naming is NamingConvention.PASCAL:
        return camelize(underscored)

    return underscored
