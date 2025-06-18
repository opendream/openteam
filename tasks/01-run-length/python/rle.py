def encode(s: str) -> str:
    """
    Run‑length encode the input string.

    >>> encode("AAB") -> "A2B1"
    """
    if s == "":
        return ""
    
    result = []
    counter = 1
    for i in range(len(s) - 1):
        if s[i] != s[i + 1]:
            result.append(s[i] + str(counter))
            counter = 1
        else:
            counter += 1

    result.append(s[-1] + str(counter))

    return "".join(result)
