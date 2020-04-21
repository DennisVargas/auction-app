SELECT count(DISTINCT Seller_ID)
FROM
  (SELECT Seller_ID
  FROM Items),
  (SELECT Rating, User_ID
    FROM Users)
WHERE Rating > 1000 AND User_ID = Seller_ID;