SELECT count(DISTINCT Seller_ID)
FROM
  (SELECT Bidder_ID
  FROM Bids),
  (SELECT Seller_ID
    FROM Items)
WHERE Bidder_ID = Seller_ID;