package rle

import (
	"strconv"
	"strings"
)

// Encode returns the run‑length encoding of UTF‑8 string s.
//
// "AAB" → "A2B1"
func Encode(s string) string {
	if s == ""{
		return ""
	}

	var builder strings.Builder
	// use rune for better storing a character like string and emoji
	enCoderRunes := []rune(s)
	for i := 0; i < len(enCoderRunes); {
		currentRune := enCoderRunes[i]
		count :=1
		for i+count < len(enCoderRunes) && enCoderRunes[i+count] == currentRune {
			count++
		}
		builder.WriteRune(currentRune)
		builder.WriteString(strconv.Itoa(count)) //convert count to string
		i += count
	}
	return builder.String()
}
