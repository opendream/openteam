def encode(s: str) -> str:
    """
    Run‑length encode the input string.

    >>> encode("AAB") -> "A2B1"
    """
    # TODO: implement
    # raise NotImplementedError("Implement me!")
    if not s:
        return ""
    
    result = []
    current_char = s[0]
    count = 1

    for char in s[1:]:
        if char == current_char:
            count += 1
        else:
            result.append(f"{current_char}{count}")
            current_char = char
            count = 1

    result.append(f"{current_char}{count}")
    return "".join(result)

print(encode("AAAaaaBBB🦄🦄🦄🦄🦄CCCCCCCCCCCC"))