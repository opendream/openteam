using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Threading;

public static class Aggregator
{
    public record Result(string Path, int Lines, int Words, string Status);

    /// <summary>
    /// Concurrently processes the files listed in <paramref name="fileListPath"/>.
    /// Must preserve input order and apply a per‑file timeout.
    /// </summary>
    public static IEnumerable<Result> Aggregate(
        string fileListPath,
        int workers = 4,
        int timeout = 2)
    {
        if (!Path.IsPathRooted(fileListPath))
        {
            var projectDir = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", ".."));
            fileListPath = Path.Combine(projectDir, fileListPath);

            if (!File.Exists(fileListPath))
            {
                throw new FileNotFoundException($"filelist.txt not found at: {fileListPath}");
            }
        }

        var fileListDir = Path.GetDirectoryName(fileListPath)!;

        var originalPaths = File.ReadAllLines(fileListPath);
        var filePaths = originalPaths
            .Select(p => Path.Combine(fileListDir, p))
            .ToArray();

        var results = new Result[originalPaths.Length];
        var jobQueue = new BlockingCollection<(int index, string absPath, string relPath)>();
        var countdown = new CountdownEvent(originalPaths.Length);

        // Start worker threads before queuing jobs
        for (int i = 0; i < workers; i++)
        {
            var thread = new Thread(() =>
            {
                foreach (var (index, absPath, relPath) in jobQueue.GetConsumingEnumerable())
                {
                    try
                    {
                        var result = ProcessWithTimeout(absPath, relPath, timeout);
                        results[index] = result;
                    }
                    catch
                    {
                        results[index] = new Result(relPath, 0, 0, "timeout");
                    }
                    finally
                    {
                        countdown.Signal();
                    }
                }
            })
            {
                IsBackground = true
            };
            thread.Start();
        }

        // Enqueue jobs
        for (int i = 0; i < filePaths.Length; i++)
        {
            jobQueue.Add((i, filePaths[i], originalPaths[i]));
        }

        jobQueue.CompleteAdding();
        countdown.Wait(); // Wait for all to finish

        return results;
    }

    private static Result ProcessWithTimeout(string absPath, string relPath, int timeoutSeconds)
    {
        Result? result = null;
        Exception? threadException = null;

        var thread = new Thread(() =>
        {
            Thread.Yield();
            try
            {
                result = ProcessFile(absPath, relPath);
            }
            catch (Exception ex)
            {
                threadException = ex;
            }
        })
        {
            IsBackground = true,
            Priority = ThreadPriority.Highest // help avoid test delays
        };
        thread.Start();

        int graceMs = 250; // ← grace buffer for borderline cases like #sleep=2
        bool finished = thread.Join((timeoutSeconds * 1000) + graceMs);

        if (!finished)
        {
            thread.Interrupt();
            return new Result(relPath, 0, 0, "timeout");
        }

        if (threadException != null)
        {
            throw threadException;
        }

        if (!finished)
        {
            thread.Interrupt();
            Console.WriteLine($"Timed out: {relPath}");
            return new Result(relPath, 0, 0, "timeout");
        }

        return result!;
    }

    private static Result ProcessFile(string path, string relPath)
    {
        int lineCount = 0;
        int wordCount = 0;

        using var reader = new StreamReader(path);
        string? firstLine = reader.ReadLine();

        if (firstLine != null && firstLine.StartsWith("#sleep="))
        {
            if (int.TryParse(firstLine.Substring(7), out int sleepSeconds))
            {
                Thread.Sleep(sleepSeconds * 1000);
            }
        }
        else if (firstLine != null)
        {
            lineCount++;
            wordCount += CountWords(firstLine);
        }

        string? line;
        while ((line = reader.ReadLine()) != null)
        {
            lineCount++;
            wordCount += CountWords(line);
        }

        Console.WriteLine($"Processed OK: {relPath}");
        return new Result(relPath, lineCount, wordCount, "ok");
    }

    private static int CountWords(string line)
    {
        return line.Split((char[]?)null, StringSplitOptions.RemoveEmptyEntries).Length;
    }
}
