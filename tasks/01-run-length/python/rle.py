def encode(s: str) -> str:
    """
    Run‑length encode the input string.

    >>> encode("AAB") -> "A2B1"
    """

    # return empty string for empty input
    if not s:
        return ""
    
    encoded = []
    count = 1
    current_char = s[0]

    # iterate through the string starting from the second character
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            # append the current character and its count 
            encoded.append(f"{current_char}{count}")
            current_char = s[i]
            count = 1
    
    # append the last character and its count
    encoded.append(f"{current_char}{count}")
    return "".join(encoded)
