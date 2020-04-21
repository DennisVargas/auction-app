-- 8. The current_price of an item must always match the amount of the most recent bid for that item

PRAGMA FOREIGN_KEYS = ON;
DROP TRIGGER IF EXISTS current_bid_match;

CREATE TRIGGER current_bid_match
AFTER INSERT ON Bids
  FOR EACH ROW
--   WHEN ((SELECT Item_ID FROM Bids) = new.Item_ID
--         --AND new.Time = (SELECT max(Time) FROM Bids)
--         AND (SELECT Item_ID FROM Items) = new.Item_ID)
  BEGIN
    UPDATE Items
    SET High_Bid = new.Amount
    WHERE Item_ID = new.Item_ID;
  END;

