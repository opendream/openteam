from pathlib import Path

# --- path to donations.db --------------------------------------------------
DB_PATH = Path(__file__).resolve().parent.parent / "donations.db"

# --- Task A ---------------------------------------------------------------
SQL_A = """
SELECT
  c.id AS campaign_id,
  COALESCE(SUM(p.amount_thb), 0) AS total_thb,
  ROUND(COALESCE(SUM(p.amount_thb), 0) * 1.0 / c.target_thb, 4) AS pct_of_target
FROM
  campaign c
LEFT JOIN
  pledge p ON c.id = p.campaign_id
GROUP BY
  c.id, c.target_thb
ORDER BY
  pct_of_target DESC,
  campaign_id ASC;
"""

# --- Task B ---------------------------------------------------------------
SQL_B = """
WITH global_ordered AS (
  SELECT amount_thb,
         ROW_NUMBER() OVER (ORDER BY amount_thb) AS rn,
         COUNT(*) OVER () AS total_count
  FROM pledge
),
thailand_ordered AS (
  SELECT p.amount_thb,
         ROW_NUMBER() OVER (ORDER BY p.amount_thb) AS rn,
         COUNT(*) OVER () AS total_count
  FROM pledge p
  JOIN donor d ON p.donor_id = d.id
  WHERE d.country = 'Thailand'
),
global_p90 AS (
  SELECT amount_thb
  FROM global_ordered
  WHERE rn = CEIL(0.9 * total_count)
),
thailand_p90 AS (
  SELECT amount_thb
  FROM thailand_ordered
  WHERE rn = CEIL(0.9 * total_count)
)
SELECT 'global' AS scope, (SELECT amount_thb FROM global_p90) AS p90_thb
UNION ALL
SELECT 'thailand' AS scope, (SELECT amount_thb FROM thailand_p90) AS p90_thb
ORDER BY scope;
"""

# --- indexes ---------------------------------------------------------------
INDEXES: list[str] = [
    # For Task A: index on pledge(campaign_id, amount_thb) speeds up sums per campaign
    "CREATE INDEX idx_pledge_campaign_amount ON pledge(campaign_id, amount_thb);",
    
    # For Task B: index on donor(id, country) and pledge(donor_id, amount_thb) speeds up join and sorting
    "CREATE INDEX idx_pledge_donor_amount ON pledge(donor_id, amount_thb);"
]
