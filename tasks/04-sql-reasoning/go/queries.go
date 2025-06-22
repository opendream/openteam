// tasks/04‑sql‑reasoning/go/queries.go
package queries

// Task A
const SQLA = `
SELECT 
    campaign_id,
    total_thb,
    ROUND(CAST(total_thb AS REAL) / target_thb, 4) AS pct_of_target
FROM (
    SELECT 
        c.id AS campaign_id,
        SUM(p.amount_thb) AS total_thb,
        c.target_thb
    FROM campaign c
    LEFT JOIN pledge p ON c.id = p.campaign_id
    GROUP BY c.id
)
ORDER BY pct_of_target DESC, campaign_id ASC
`

// Task B
const SQLB = `
WITH GlobalRanks AS (
    SELECT 
        amount_thb,
        ROW_NUMBER() OVER (ORDER BY amount_thb) AS row_num,
        COUNT(*) OVER () AS total_count
    FROM pledge
),
ThailandRanks AS (
    SELECT 
        p.amount_thb,
        ROW_NUMBER() OVER (ORDER BY p.amount_thb) AS row_num,
        COUNT(*) OVER () AS total_count
    FROM pledge p
    JOIN donor d ON p.donor_id = d.id
    WHERE d.country = 'Thailand'
)
SELECT 'global' AS scope, amount_thb AS p90_thb
FROM GlobalRanks
WHERE row_num = CAST((total_count * 0.9) + 0.999999 AS INTEGER)

UNION ALL

SELECT 'thailand' AS scope, amount_thb AS p90_thb
FROM ThailandRanks
WHERE row_num = CAST((total_count * 0.9) + 0.999999 AS INTEGER)
ORDER BY scope
`

var Indexes = []string{
	`CREATE INDEX idx_pledge_campaign_id_amount ON pledge (campaign_id, amount_thb)`,
	`CREATE INDEX idx_pledge_donor_id_amount ON pledge (donor_id, amount_thb)`,
}
