def encode(s: str) -> str:
    """
    Run-length encode the input string.
    
    Key Requirements:
    - Case-sensitive: Distinguishes between uppercase and lowercase characters
    - Multi-digit counts: Handles sequences of any length (100, 1000, etc.)
    - Full Unicode support: Works with all Unicode characters including Thai, Arabic, Chinese, emojis
    - O(n) time complexity: Linear performance, single pass through input
    - No third-party RLE libraries: Pure Python implementation
    
    Args:
        s (str): Input string to encode
        
    Returns:
        str: Run-length encoded string where each character is followed by its count
        
    Examples:
        >>> encode("AAB")
        'A2B1'
        >>> encode("Hello")
        'H1e1l2o1'
        >>> encode("AAAaaaBBB")
        'A3a3B3'
        >>> encode("สวัสดี")  # Thai text
        'ส1ว1ั1ส1ด1ี1'
        >>> encode("🚀🚀🚀")  # Emojis
        '🚀3'
        >>> encode("A" * 100)  # Multi-digit count
        'A100'
    """
    if not isinstance(s, str) or s is None or s == "":
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
