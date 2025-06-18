using System;
using System.Text;
using System.Globalization;

namespace Rle;

public static class Encoder
{
    // Return run‑length encoding of `input`.
    public static string Encode(string input)
    {
        if (string.IsNullOrEmpty(input))
            return string.Empty;

        var sb = new StringBuilder();
        var textEnum = StringInfo.GetTextElementEnumerator(input);

        if (!textEnum.MoveNext())
            return string.Empty;

        string prev = textEnum.GetTextElement();
        int count = 1;

        while (textEnum.MoveNext())
        {
            string curr = textEnum.GetTextElement();
            if (curr == prev)
            {
                count++;
            }
            else
            {
                sb.Append(prev);
                sb.Append(count);
                prev = curr;
                count = 1;
            }
        }

        sb.Append(prev);
        sb.Append(count);

        return sb.ToString();
    }
}
