-- 10. No auction may have two bids at the exact same time

PRAGMA FOREIGN_KEYS = ON;
DROP TRIGGER IF EXISTS bid_time;

CREATE TRIGGER bid_time
BEFORE INSERT ON Bids
  FOR EACH ROW
  WHEN ((SELECT Item_ID FROM Bids) = new.Item_ID AND (SELECT Time FROM Bids) = new.Time)
  BEGIN
    SELECT RAISE(ABORT, 'Cannot enter two bids for the same item with the exact same time.');
  END;