def encode(s: str) -> str:
    """
    Run‑length encode the input string.

    >>> encode("AAB") -> "A2B1"
    """
    # TODO: implement
    # raise NotImplementedError("Implement me!")

    count_dict: dict[str, int] = {}
    for character in s:
        count_dict[character] = count_dict.setdefault(character, 0) + 1
    concate_str: str = ''
    for character, count_value in count_dict.items():
        concate_str = concate_str + character + str(count_value) 
    return concate_str
        

if __name__ == "__main__":
    # encode("")                              → ""
    # encode("XYZ")                           → "X1Y1Z1"
    # encode("AAAaaaBBB🦄🦄🦄🦄🦄CCCCCCCCCCCC") → "A3a3B3🦄5C12"
    # encode("HAAAAPPY🦄")                    → "H1A4P2Y1🦄1"
    
    print(encode("AAAaaaBBB🦄🦄🦄🦄🦄CCCCCCCCCCCC"))