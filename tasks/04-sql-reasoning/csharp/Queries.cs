// tasks/04‑sql‑reasoning/csharp/Queries.cs
namespace SqlReasoning
{
    public static class Queries
    {
        public const string SQL_A = @"
            SELECT
                c.id AS campaign_id,
                COALESCE(SUM(p.amount_thb), 0) AS total_thb,
                ROUND(COALESCE(SUM(p.amount_thb), 0) * 1.0 / c.target_thb, 4) AS pct_of_target
            FROM campaign c
            LEFT JOIN pledge p ON c.id = p.campaign_id
            GROUP BY c.id
            ORDER BY pct_of_target DESC, campaign_id ASC;
        ";

        public const string SQL_B = @"
            WITH ranked_global AS (
                SELECT
                    amount_thb,
                    ROW_NUMBER() OVER (ORDER BY amount_thb) AS rnk,
                    COUNT(*) OVER () AS total
                FROM pledge
            ),
            ranked_thailand AS (
                SELECT
                    p.amount_thb,
                    ROW_NUMBER() OVER (ORDER BY p.amount_thb) AS rnk,
                    COUNT(*) OVER () AS total
                FROM pledge p
                JOIN donor d ON p.donor_id = d.id
                WHERE d.country = 'Thailand'
            )
            SELECT 'global' AS scope, (
                SELECT amount_thb
                FROM ranked_global
                WHERE rnk = CEIL(0.9 * total)
            ) AS p90_thb
            UNION ALL
            SELECT 'thailand' AS scope, (
                SELECT amount_thb
                FROM ranked_thailand
                WHERE rnk = CEIL(0.9 * total)
            ) AS p90_thb;
        ";

        public static readonly string[] INDEXES =
        [
            "CREATE INDEX idx_pledge_campaign_id ON pledge(campaign_id)",
            "CREATE INDEX idx_pledge_donor_id_amount ON pledge(donor_id, amount_thb)"
        ];   // skipped
    }
}
