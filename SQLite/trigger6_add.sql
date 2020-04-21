-- 14. Any new bid for a particular item must have a higher amount than any of the previous bids for that particular item.

PRAGMA FOREIGN_KEYS = ON;
DROP TRIGGER IF EXISTS new_bid_is_high;

CREATE TRIGGER new_bid_is_high
BEFORE INSERT ON Bids
  FOR EACH ROW
  WHEN new.Amount < (SELECT max(Amount) FROM (SELECT Amount, Item_ID FROM Bids WHERE Item_ID = new.Item_ID))
  BEGIN
    SELECT RAISE(ABORT, 'New bids must be greater than previous bids.');
  END;