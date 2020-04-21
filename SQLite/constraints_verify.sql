-- 1. Verify no duplicate user names (NECESSARY)
  SELECT u1.User_ID
  FROM (
  SELECT u2.User_ID, count(u2.User_ID)as cnt1
  FROM Users as u2
  GROUP BY User_ID
  ORDER BY cnt1
  )AS u1
  WHERE cnt1 > 1;

-- 2. Verify bidders and sellers are users
--  SELECT u1.User_ID
--  FROM Users AS u1
--  WHERE u1.User_ID NOT IN (
--    SELECT b1.Bidder_ID
--    FROM Bids AS b1
--  ) AND u1.User_ID NOT IN(
--    SELECT i1.Seller_ID
--    FROM Items AS i1
--  );

-- 3. No two items share same item id
--     SELECT i1.Item_ID
--     FROM (
--       SELECT i2.Item_ID, count(i2.Item_ID) AS cnt1
--       FROM Items AS i2
--       GROUP BY i2.Item_ID
--       ORDER BY cnt1
--     ) AS i1
--     WHERE cnt1 > 1;

-- 4. Every bid corresponds to an actual item (NECESSARY)
  SELECT b1.Item_ID
  FROM Bids AS b1
  WHERE b1.Item_ID NOT IN (
  SELECT i1.Item_ID
  FROM Items AS i1
  );

-- 5. The items for a given category must exist (NECESSARY)
  SELECT DISTINCT c1.Item_ID
  FROM Categories as c1
  WHERE c1.Item_ID NOT IN (
    SELECT i1.Item_ID
    FROM Items AS i1
  );

-- 6. An item cannot belong to a particular category more than once
  SELECT i1, t1.cnt1, t1.cnt2
      FROM (
    SELECT c1.Item_ID AS i1, count(c1.Item_ID) As cnt1, count(c1.Category) AS cnt2
    FROM Categories as c1
    GROUP BY c1.Item_ID
  ) AS t1
WHERE cnt1 != cnt2
GROUP BY i1;


-- 7. The end time for an auction must always be after its start time
  SELECT DISTINCT i1.Item_ID
  FROM Items as i1
  WHERE i1.Start_Time > i1.End_Time;  -- Just copying general idea

-- 8. No auction may have two bids at the exact same time
--   SELECT i1.Item_ID
--   FROM Items AS i1, Bids AS b1, Bids AS b2
--   WHERE b1.Time = b2.Time AND b1.Bidder_ID != b2.Bidder_ID
--   GROUP BY i1.Item_ID;

-- 12. No user can make a bid of the same
-- amount to the same item more than once
--  SELECT b1.Item_ID, b1.Amount, b1.Bidder_ID
--  FROM Bids AS b1
--  WHERE Amount = Amount AND Time =  Time AND Item_ID = Item_ID;