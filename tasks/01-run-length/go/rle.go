package rle

import (
	"strconv"
	"strings"
)

// Encode returns the run‑length encoding of UTF‑8 string s.
//
// "AAB" → "A2B1"
func Encode(s string) string {

	if len(s) == 0 {
		return ""
	}

	var builder strings.Builder
	count := 1
	runes := []rune(s)

	for i := 1; i < len(runes); i++ {
		if runes[i] == runes[i-1] {
			count++
		} else {
			builder.WriteRune(runes[i-1])
			builder.WriteString(strconv.Itoa(count))
			count = 1
		}
	}

	builder.WriteRune(runes[len(runes)-1])
	builder.WriteString(strconv.Itoa(count))

	return builder.String()
}
