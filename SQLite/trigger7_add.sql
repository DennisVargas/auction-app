-- 15. All new bids must be placed at the time which matches the current time of your AuctionBase system.

PRAGMA FOREIGN_KEYS = ON;
DROP TRIGGER IF EXISTS new_bid_current_time;

CREATE TRIGGER new_bid_current_time
BEFORE INSERT ON Bids
  FOR EACH ROW
  WHEN (new.Time != (SELECT Sys_Time FROM Time))
  BEGIN
    SELECT RAISE(ABORT, 'New bids must be entered at the current system time.');
  END;