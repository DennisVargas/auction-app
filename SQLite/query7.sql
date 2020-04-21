SELECT count(DISTINCT Category)
FROM
  (SELECT Item_ID as I_ID, High_Bid
  FROM Items
  WHERE High_Bid > 100),
  (SELECT Category, Item_ID as C_ID
    FROM Categories)
WHERE I_ID = C_ID;

