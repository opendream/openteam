def encode(s: str) -> str:
    """
    Run-length encode the input string.

    >>> encode("AAB") -> "A2B1"
    """
    if not s:
        return ""
    result = []
    prev = s[0]
    count = 1
    for c in s[1:]:
        if c == prev:
            count += 1
        else:
            result.append(f"{prev}{count}")
            prev = c
            count = 1
    result.append(f"{prev}{count}")
    return ''.join(result)
