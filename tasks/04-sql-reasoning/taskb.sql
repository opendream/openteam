WITH all_pledges AS (
  SELECT 'global' AS scope, amount_thb FROM pledge
  UNION ALL
  SELECT 'thailand' AS scope, p.amount_thb
  FROM pledge p
  JOIN donor d ON d.id = p.donor_id
  WHERE d.country = 'Thailand'
),
ranked AS (
  SELECT
    scope,
    amount_thb,
    ROW_NUMBER() OVER (PARTITION BY scope ORDER BY amount_thb) AS rn,
    COUNT(*) OVER (PARTITION BY scope) AS total
  FROM all_pledges
),
positioned AS (
  SELECT
    scope,
    amount_thb,
    rn,
    total,
    0.9 * (total - 1) + 1 AS pos
  FROM ranked
),
interpolated AS (
  SELECT
    p1.scope,
    p1.amount_thb AS lower_val,
    p1.rn,
    p1.pos,
    p2.amount_thb AS upper_val
  FROM positioned p1
  LEFT JOIN positioned p2
    ON p1.scope = p2.scope AND p2.rn = p1.rn + 1
  WHERE p1.rn = CAST(p1.pos AS INTEGER )
)
SELECT
  scope,
  CAST(ROUND(
    CASE
      WHEN pos = rn THEN lower_val
      ELSE lower_val + (pos - rn) * (upper_val - lower_val)
    END
  ) AS INT) AS p90_thb
FROM interpolated
ORDER BY scope;
