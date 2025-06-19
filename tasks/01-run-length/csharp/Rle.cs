using System;
using System.Text;
namespace Rle;

public static class Encoder
{
    // Return run‑length encoding of `input`.
    public static string Encode(string input)
    {
        if (string.IsNullOrEmpty(input))
        {
            return string.Empty;
        }
        StringBuilder result = new StringBuilder();
        int count = 1;
        string prevChar = "";
        int i = 0;
        while (i < input.Length)
        {

            string currentChar;
            if (char.IsHighSurrogate(input[i]) && i + 1 < input.Length && char.IsLowSurrogate(input[i + 1]))
            {
                currentChar = new string(new[] { input[i], input[i + 1] });
                i += 2;
            }
            else
            {
                currentChar = input[i].ToString();
                i++;
            }

            if (currentChar == prevChar)
            {
                count++;
            }
            else
            {
                if (prevChar != "")
                {
                    result.Append(prevChar + count);
                }
                prevChar = currentChar;
                count = 1;
            }
        }
        if (prevChar != "")
        {
            result.Append(prevChar + count);
        }

        return result.ToString();
    }
}
