SELECT Item_ID
FROM
  (SELECT max(High_Bid) AS high, Item_ID, High_Bid
    FROM Items)
WHERE High_Bid=high;