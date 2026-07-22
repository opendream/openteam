from itertools import groupby
import unicodedata

def encode(s: str) -> str:
    chars = get_graphemes(s)
    result = []
    for char, group in groupby(chars):
        count = sum(1 for _ in group)
        result.append(f"{char}{count}")

    return "".join(result)

def get_graphemes(text: str):
    graphemes = []
    current = ""

    for char in text:
        category = unicodedata.category(char)

        if not current:
            current = char
        elif (
            category == "Mn"
            or char == "\u200d"
            or (current and current[-1] == "\u200d")
        ):
            current += char
        else:
            graphemes.append(current)
            current = char

    if current:
        graphemes.append(current)

    return graphemes