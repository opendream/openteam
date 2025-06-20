def encode(s: str) -> str:
    if not s:
        return ""

    result = []
    current = s[0]
    count = 1

    for char in s[1:]:
        if char == current:
            count += 1
        else:
            result.append(current + str(count))
            current = char
            count = 1

    result.append(current + str(count))

    return "".join(result)
