using System.Threading;

namespace BuggyLib;

public static class BuggyCounter
{
    private static long _current = 0;

    public static long NextId()
    {
        return Interlocked.Increment(ref _current) - 1;
    }
}
